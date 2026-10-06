"""Reproducibility capture: config hash, git commit, environment snapshot.

- **Label:** ESTABLISHED
- **Phase:** 02
- **Config flag:** none.

Purpose
-------
Every experiment must be attributable: which config, which code, which machine.
These helpers produce the record stored alongside JSONL logs and checkpoints
(``docs/EXPERIMENTS.md``).

Interface
---------
``canonical_json(obj) -> str``
    Deterministic JSON (sorted keys, compact separators, sanitised values).

``config_hash(obj) -> str``
    SHA-256 hex digest (64 chars) of :func:`canonical_json`. Accepts a mapping,
    dataclass, list, or a plain string.

``file_hash(path) -> str``
    SHA-256 hex digest of a file's bytes (dataset/tokenizer artefacts).

``git_snapshot(repo_dir=None) -> dict``
    ``{"available", "commit", "branch", "dirty", "describe"}`` — never raises:
    a machine without git or without a repo reports ``available: False``.

``environment_snapshot() -> dict``
    Python/torch/CUDA/platform facts. Never raises.

``capture(obj=None, repo_dir=None) -> dict``
    Combined record: ``{"config_hash", "config", "git", "environment"}``.

Tensor shapes: **none** — metadata only.

Notes / edge cases / risks
--------------------------
* Hashing is over the *canonical* form, so key order and float formatting never
  change a hash; adding a key always does.
* ``git`` subprocesses are time-limited (5 s) and their failures are reported, not raised —
  a training run must not die because ``git`` is missing.
* Non-finite floats are stringified (same rule as ``utils/logging``) so hashes stay stable.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import subprocess
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Mapping

_GIT_TIMEOUT_S = 5
_UINT32 = 2**32


def _sanitize(obj: Any, depth: int = 0) -> Any:
    """JSON-safe conversion (same semantics as ``utils.logging._sanitize``)."""
    if depth > 8:
        return str(obj)
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
    if is_dataclass(obj) and not isinstance(obj, type):
        return _sanitize(asdict(obj), depth + 1)
    if isinstance(obj, Mapping):
        return {str(k): _sanitize(v, depth + 1) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set, frozenset)):
        return [_sanitize(v, depth + 1) for v in obj]
    if isinstance(obj, Path):
        return str(obj)
    if hasattr(obj, "detach") and hasattr(obj, "dtype"):  # torch.Tensor
        try:
            if obj.numel() == 1:
                return _sanitize(obj.detach().cpu().item(), depth + 1)
            return {"shape": [int(d) for d in obj.shape], "dtype": str(obj.dtype)}
        except Exception:  # pragma: no cover - defensive
            return str(obj)
    return str(obj)


def canonical_json(obj: Any) -> str:
    """Deterministic JSON encoding of ``obj``.

    Output: ``str`` — sorted keys, separators ``(",", ":")``, ASCII-safe, NaN-free.
    """
    return json.dumps(
        _sanitize(obj),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def config_hash(obj: Any) -> str:
    """SHA-256 of :func:`canonical_json` for a config object.

    Input: mapping / dataclass / list / str. Output: 64-char lowercase hex ``str``.
    """
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def file_hash(path: str | Path) -> str:
    """SHA-256 of a file's bytes, streamed in 1 MiB chunks.

    Input: file path. Output: 64-char lowercase hex ``str``.

    Raises
    ------
    FileNotFoundError
        The path does not exist.
    IsADirectoryError
        The path is a directory.
    """
    target = Path(path)
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git(args: list[str], repo_dir: str | Path | None) -> subprocess.CompletedProcess[str] | None:
    command = ["git", *args]
    try:
        return subprocess.run(
            command,
            cwd=str(repo_dir) if repo_dir is not None else None,
            capture_output=True,
            text=True,
            timeout=_GIT_TIMEOUT_S,
        )
    except (OSError, subprocess.SubprocessError):
        return None


def git_snapshot(repo_dir: str | Path | None = None) -> dict[str, Any]:
    """Capture the git state of ``repo_dir`` (default: current working directory).

    Output: ``dict`` with keys ``available (bool)``, ``commit (str|None)``,
    ``branch (str|None)``, ``dirty (bool|None)``, ``describe (str|None)``.

    Never raises: missing git or a non-repo directory yields ``available: False``.
    """
    result = _git(["rev-parse", "--is-inside-work-tree"], repo_dir)
    if result is None or result.returncode != 0 or result.stdout.strip() != "true":
        return {
            "available": False,
            "commit": None,
            "branch": None,
            "dirty": None,
            "describe": None,
        }

    def _out(args: list[str]) -> str | None:
        proc = _git(args, repo_dir)
        if proc is None or proc.returncode != 0:
            return None
        value = proc.stdout.strip()
        return value or None

    status = _git(["status", "--porcelain"], repo_dir)
    dirty: bool | None = None
    if status is not None and status.returncode == 0:
        dirty = bool(status.stdout.strip())

    return {
        "available": True,
        "commit": _out(["rev-parse", "HEAD"]),
        "branch": _out(["rev-parse", "--abbrev-ref", "HEAD"]),
        "dirty": dirty,
        "describe": _out(["describe", "--always", "--dirty"]),
    }


def environment_snapshot() -> dict[str, Any]:
    """Capture interpreter/OS/framework facts.

    Output: ``dict`` with keys ``python_version, python_implementation, platform,
    machine, executable, torch_version, torch_cuda_version, cuda_available,
    gpu_count, gpu_names``. All values are JSON-safe strings/ints/bools/lists.

    Never raises: if torch is not importable the torch fields are ``None``/``False``.
    """
    snapshot: dict[str, Any] = {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "executable": sys.executable,
        "torch_version": None,
        "torch_cuda_version": None,
        "cuda_available": False,
        "gpu_count": 0,
        "gpu_names": [],
    }
    try:
        import torch
    except Exception:  # pragma: no cover - torch is a hard dep, but never crash here
        return snapshot

    snapshot["torch_version"] = str(torch.__version__)
    snapshot["cuda_available"] = bool(torch.cuda.is_available())
    cuda_version = getattr(torch.version, "cuda", None)
    snapshot["torch_cuda_version"] = str(cuda_version) if cuda_version else None
    if snapshot["cuda_available"]:
        try:
            names = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
            snapshot["gpu_count"] = len(names)
            snapshot["gpu_names"] = names
        except Exception:  # pragma: no cover - defensive
            pass
    return snapshot


def capture(
    obj: Any = None, repo_dir: str | Path | None = None
) -> dict[str, Any]:
    """Build the full reproducibility record for an experiment.

    Parameters
    ----------
    obj : optional
        Config to hash and embed (mapping/dataclass/list/str). ``None`` skips it
        and reports ``config_hash: None``.
    repo_dir : str | Path, optional
        Repository to snapshot (default: current working directory).

    Output: ``dict`` with keys ``config_hash, config, git, environment`` — all
    JSON-safe. Never raises.
    """
    record: dict[str, Any] = {
        "config_hash": None,
        "config": None,
        "git": git_snapshot(repo_dir),
        "environment": environment_snapshot(),
    }
    if obj is not None:
        record["config_hash"] = config_hash(obj)
        record["config"] = _sanitize(obj)
    return record


__all__ = [
    "canonical_json",
    "config_hash",
    "file_hash",
    "git_snapshot",
    "environment_snapshot",
    "capture",
]
