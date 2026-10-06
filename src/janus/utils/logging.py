"""Structured JSON-lines logging.

- **Label:** ESTABLISHED
- **Phase:** 02
- **Config flag:** none (log destination comes from the caller / YAML).

Purpose
-------
One JSON object per line (JSONL) so training logs are greppable, parseable and
diffable. Library code must never ``print`` (``docs/CODING_STANDARDS.md``).

Interface
---------
``JsonlLogger(path, *, run_id=None, level="INFO", console=False, context=None)``
    Opens/appends ``path`` (parent directories are created).
``logger.log(level, event, **fields)`` / ``logger.debug|info|warning|error|critical(event, **fields)``
    Write one record. ``event`` is a short stable string; everything else is a field.
``logger.set_context(**fields)``   attach persistent fields (e.g. ``experiment_id``).
``logger.log_exception(event, **fields)``  attach the active traceback.
``logger.close()`` / context-manager exit  flush and close the file.
``read_records(path) -> list[dict]``  parse a JSONL file back into dicts.

Each line: ``{"ts", "level", "event", "run_id"?, <context>, <fields>}``.
``ts`` is ISO-8601 UTC with ``Z``.

Tensor shapes: **none** — no tensors are produced. A logged ``torch.Tensor`` field is
*converted*: a 0-dim/1-element tensor becomes a Python scalar; anything else becomes
``{"shape": [B, T, ...], "dtype": "torch.float32"}`` (rank and sizes only, no data).

Notes / edge cases / risks
--------------------------
* The output is *strict* JSON: non-finite floats are written as ``"NaN"`` /
  ``"Infinity"`` / ``"-Infinity"`` strings rather than the invalid ``NaN`` literal,
  so ``json.loads`` always succeeds.
* Depth is capped (8) and a cycle guard is in place; a malformed record is stringified
  rather than crashing a training run.
* Level filtering: records below ``level`` are dropped (not written to file or console).
* Reserved keys ``ts``, ``level``, ``event``, ``run_id`` are rejected with
  :class:`LogError` so a field can never shadow the record envelope.
* Console mirroring uses the stdlib ``janus.jsonl`` logger (no bare prints).
"""

from __future__ import annotations

import json
import logging as stdlib_logging
import math
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping

LEVELS: dict[str, int] = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}
RESERVED_KEYS: frozenset[str] = frozenset({"ts", "level", "event", "run_id"})
_MAX_DEPTH = 8
_CONSOLE_LOGGER_NAME = "janus.jsonl"


class LogError(RuntimeError):
    """Raised for invalid logging usage (bad level, reserved key, closed logger)."""


def _json_default(obj: Any) -> str:
    """Last-resort encoder for types ``json`` cannot handle."""
    # Path / os.PathLike
    if isinstance(obj, Path):
        return str(obj)
    # dataclass
    if hasattr(obj, "__dataclass_fields__"):
        from dataclasses import asdict

        return json.dumps(asdict(obj), default=_json_default, allow_nan=False)
    # numpy scalar / array (numpy is already a hard dependency of torch)
    item = getattr(obj, "item", None)
    if callable(item) and getattr(obj, "size", 1) == 1:
        return _json_default(item())
    shape = getattr(obj, "shape", None)
    dtype = getattr(obj, "dtype", None)
    if shape is not None and dtype is not None:
        return {"shape": [int(d) for d in shape], "dtype": str(dtype)}
    return str(obj)


def _sanitize(obj: Any, depth: int = 0, seen: set[int] | None = None) -> Any:
    """Convert ``obj`` into something ``json.dumps(..., allow_nan=False)`` accepts.

    Output: JSON-safe ``dict``/``list``/``str``/``int``/``float``/``bool``/``None``.
    Non-finite floats become strings; tensors become scalars or shape records.
    """
    if depth > _MAX_DEPTH:
        return str(obj)
    seen = seen if seen is not None else set()

    if obj is None or isinstance(obj, (bool, int, str)):
        return obj

    if isinstance(obj, float):
        if obj != obj:
            return "NaN"
        if obj == float("inf"):
            return "Infinity"
        if obj == float("-inf"):
            return "-Infinity"
        return obj

    # torch.Tensor → scalar (rank 0 or single element), else shape/dtype record
    if hasattr(obj, "detach") and hasattr(obj, "shape") and hasattr(obj, "dtype"):
        try:
            if obj.numel() == 1:
                value = obj.detach().cpu().item()
                return _sanitize(value, depth + 1, seen)
            return {"shape": [int(d) for d in obj.shape], "dtype": str(obj.dtype)}
        except Exception:  # pragma: no cover - defensive: logging must not crash
            return str(obj)

    if isinstance(obj, Mapping):
        obj_id = id(obj)
        if obj_id in seen:
            return "<cycle>"
        seen = seen | {obj_id}
        return {str(k): _sanitize(v, depth + 1, seen) for k, v in obj.items()}

    if isinstance(obj, (list, tuple, set, frozenset)):
        obj_id = id(obj)
        if obj_id in seen:
            return "<cycle>"
        seen = seen | {obj_id}
        return [_sanitize(v, depth + 1, seen) for v in obj]

    if isinstance(obj, Path):
        return str(obj)

    # dataclass → plain dict (avoid double-encoding through json.dumps)
    if hasattr(obj, "__dataclass_fields__"):
        from dataclasses import asdict

        return _sanitize(asdict(obj), depth + 1, seen)

    # numpy scalar/array, torch dtype/device, datetime, anything else
    try:
        return _sanitize(_json_default(obj), depth + 1, seen)
    except Exception:  # pragma: no cover - defensive
        return str(obj)


def _reject_reserved(fields: dict[str, Any]) -> None:
    """Raise :class:`LogError` if a field would shadow the record envelope."""
    clash = RESERVED_KEYS.intersection(fields)
    if clash:
        raise LogError(f"reserved log keys cannot be used as fields: {sorted(clash)}")


def _console_logger() -> stdlib_logging.Logger:
    """Return the shared stdlib logger used for console mirroring (handler added once)."""
    logger = stdlib_logging.getLogger(_CONSOLE_LOGGER_NAME)
    if not any(isinstance(h, stdlib_logging.StreamHandler) for h in logger.handlers):
        handler = stdlib_logging.StreamHandler()
        handler.setFormatter(stdlib_logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.setLevel(stdlib_logging.INFO)
        logger.propagate = False
    return logger


class JsonlLogger:
    """Append-only JSONL writer with level filtering and optional console mirroring.

    Parameters
    ----------
    path : str | Path
        Destination file. Parent directories are created. Nothing is hard-coded —
        the caller supplies it (from YAML config or CLI).
    run_id : str, optional
        Experiment/run identifier written into every record.
    level : str
        One of :data:`LEVELS`; records below it are dropped.
    console : bool
        Mirror records to stderr via the ``janus.jsonl`` stdlib logger.
    context : Mapping, optional
        Persistent fields merged into every record (e.g. ``experiment_id``).
    """

    def __init__(
        self,
        path: str | Path,
        *,
        run_id: str | None = None,
        level: str = "INFO",
        console: bool = False,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        if not isinstance(level, str) or level.upper() not in LEVELS:
            raise LogError(f"unknown level {level!r}; expected one of {tuple(LEVELS)}")
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self._path.open("a", encoding="utf-8", newline="\n")
        self._level = LEVELS[level.upper()]
        self._level_name = level.upper()
        self._run_id = run_id
        self._console = bool(console)
        self._context: dict[str, Any] = dict(context or {})
        self._lock = threading.Lock()
        self._closed = False

    # -- properties -------------------------------------------------------
    @property
    def path(self) -> Path:
        """Destination file path (as passed by the caller)."""
        return self._path

    @property
    def level(self) -> str:
        """Active level name, e.g. ``"INFO"``."""
        return self._level_name

    @property
    def closed(self) -> bool:
        """``True`` once :meth:`close` ran."""
        return self._closed

    def set_context(self, **fields: Any) -> None:
        """Merge persistent fields into every subsequent record.

        Reserved keys (:data:`RESERVED_KEYS`) raise :class:`LogError`.
        """
        clash = RESERVED_KEYS.intersection(fields)
        if clash:
            raise LogError(f"reserved log keys cannot be used as context: {sorted(clash)}")
        self._context.update(fields)

    # -- writing ----------------------------------------------------------
    def log(self, level: str, event: str, **fields: Any) -> bool:
        """Write one record.

        Parameters
        ----------
        level : str
            One of :data:`LEVELS`.
        event : str
            Stable event name, e.g. ``"train_step"``.
        **fields
            Arbitrary JSON-safe payload (tensors/NaN are converted).

        Returns
        -------
        bool
            ``True`` if the record passed the level filter and was written,
            ``False`` if it was filtered out.

        Raises
        ------
        LogError
            Unknown level, non-string event, reserved field key, or closed logger.
        """
        if self._closed:
            raise LogError(f"logger for {self._path} is closed")
        if not isinstance(level, str) or level.upper() not in LEVELS:
            raise LogError(f"unknown level {level!r}; expected one of {tuple(LEVELS)}")
        if not isinstance(event, str) or not event:
            raise LogError(f"event must be a non-empty str, got {event!r}")
        _reject_reserved(fields)

        numeric = LEVELS[level.upper()]
        if numeric < self._level:
            return False

        record: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            ),
            "level": level.upper(),
            "event": event,
        }
        if self._run_id is not None:
            record["run_id"] = self._run_id
        record.update(self._context)
        record.update(fields)

        line = json.dumps(
            _sanitize(record),
            ensure_ascii=False,
            allow_nan=False,
            default=_json_default,
        )

        with self._lock:
            if self._closed:
                raise LogError(f"logger for {self._path} is closed")
            self._file.write(line + "\n")
            self._file.flush()
            if self._console:
                _console_logger().info(line)
        return True

    def debug(self, event: str, **fields: Any) -> bool:
        """Write a ``DEBUG`` record. Returns whether it was written."""
        _reject_reserved(fields)
        return self.log("DEBUG", event, **fields)

    def info(self, event: str, **fields: Any) -> bool:
        """Write an ``INFO`` record. Returns whether it was written."""
        _reject_reserved(fields)
        return self.log("INFO", event, **fields)

    def warning(self, event: str, **fields: Any) -> bool:
        """Write a ``WARNING`` record. Returns whether it was written."""
        _reject_reserved(fields)
        return self.log("WARNING", event, **fields)

    def error(self, event: str, **fields: Any) -> bool:
        """Write an ``ERROR`` record. Returns whether it was written."""
        _reject_reserved(fields)
        return self.log("ERROR", event, **fields)

    def critical(self, event: str, **fields: Any) -> bool:
        """Write a ``CRITICAL`` record. Returns whether it was written."""
        _reject_reserved(fields)
        return self.log("CRITICAL", event, **fields)

    def log_exception(self, event: str, **fields: Any) -> bool:
        """Write an ``ERROR`` record carrying the active traceback (if any).

        ``traceback`` field is added when called inside an ``except`` block.
        Returns whether the record was written.
        """
        try:
            import traceback as _traceback

            tb = _traceback.format_exc()
            if tb and tb.strip() != "NoneType: None":
                fields.setdefault("traceback", tb)
        except Exception:  # pragma: no cover - defensive
            pass
        return self.log("ERROR", event, **fields)

    # -- lifecycle --------------------------------------------------------
    def close(self) -> None:
        """Flush and close the file. Safe to call twice."""
        with self._lock:
            if not self._closed:
                self._file.flush()
                self._file.close()
                self._closed = True

    def __enter__(self) -> JsonlLogger:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc is not None and not self._closed:
            try:
                self.log_exception("logger.closed_with_exception")
            except LogError:  # pragma: no cover - never mask the original error
                pass
        self.close()

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"JsonlLogger(path={str(self._path)!r}, level={self._level_name!r}, closed={self._closed})"


def read_records(path: str | Path) -> list[dict[str, Any]]:
    """Parse a JSONL file back into records.

    Input: file path. Output: ``list[dict]`` — one dict per non-empty line.
    Raises :class:`LogError` (with the line number) on malformed JSON.
    """
    file_path = Path(path)
    records: list[dict[str, Any]] = []
    with file_path.open("r", encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                raise LogError(f"{file_path}:{number}: malformed JSONL line: {exc}") from exc
            if not isinstance(parsed, dict):
                raise LogError(f"{file_path}:{number}: JSONL record is not an object")
            records.append(parsed)
    return records


def iter_records(path: str | Path) -> Iterator[dict[str, Any]]:
    """Lazily yield records from a JSONL file (same parsing rules as :func:`read_records`)."""
    yield from read_records(path)


__all__ = [
    "LEVELS",
    "RESERVED_KEYS",
    "LogError",
    "JsonlLogger",
    "read_records",
    "iter_records",
]
