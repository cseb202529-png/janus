"""Data-pipeline configuration loaded from YAML, with validation.

- **Label:** ESTABLISHED
- **Phase:** 02
- **Config flag:** none (this *is* the config layer).

Purpose
-------
Describe where data comes from and how it is filtered, deduplicated, sharded and
packed — plus a pointer to the tokenizer — with everything validated up front.

Interface
---------
``DataConfig(...)``                validates itself in ``__post_init__``
``DataConfig.from_yaml(path)``     YAML → config
``DataConfig.from_dict(data)``     dict → config (unknown keys rejected)
``config.to_dict() -> dict``       config → nested plain dict
``config.validate() -> None``      re-run validation (raises ``ConfigError``)

Tensor shapes: **none** — this module builds no tensors.

Defaults (documented; asserted in ``tests/unit/config/test_data_config.py``)
---------------------------------------------------------------------------
============================  ====================  ==========================
Field                         Default               Valid range
============================  ====================  ==========================
``sources``                   ``[]``                list[str] (dataset record paths)
``tokenizer_ref``             ``None``              None, or non-empty str
``min_doc_len``               ``1``                 int >= 1
``max_doc_len``               ``100000``            int >= min_doc_len
``language_filter``           ``["en"]``            list[str], may be empty (= off)
``min_quality_score``         ``0.0``               float in [0, 1]
``safety_filter``             ``True``              bool
``contamination_filter``      ``True``              bool
``dedup``                     ``True``              bool
``dedup_algorithm``           ``"minhash"``         exact|minhash|simhash
``dedup_threshold``           ``0.8``               float in [0, 1]
``shard_size``                ``100000``            int >= 1 (tokens per shard)
``packing_length``            ``512``               int >= 1 (tokens per packed seq)
``max_tokens``                ``None``              None, or int >= 1
``cache_dir``                 ``None``              None, or non-empty str path
``drop_remainder``            ``True``              bool
============================  ====================  ==========================

Notes / edge cases / risks
--------------------------
* ``tokenizer_ref`` and ``cache_dir`` default to ``null`` — no path or tokenizer
  name is hard-coded (``AGENTS.md`` §3.7); later phases raise if they are needed.
* ``sources`` reference *dataset version records* under ``datasets/`` per
  ``docs/DATA_POLICY.md``; this config stores the references, not the data.
* ``max_tokens``/``max_documents`` caps exist for the 100 → 1K → 10K scale ladder.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping

import yaml

from janus.config.model_config import (
    ConfigError,
    _reject_unknown,
    _require_bool,
    _require_choice,
    _require_float,
    _require_int,
)

DEDUP_ALGORITHMS: tuple[str, ...] = ("exact", "minhash", "simhash")


def _require_str_list(name: str, value: Any) -> list[str]:
    if not isinstance(value, (list, tuple)):
        raise ConfigError(f"{name} must be a list of str, got {type(value).__name__}")
    items = list(value)
    for index, item in enumerate(items):
        if not isinstance(item, str) or not item.strip():
            raise ConfigError(f"{name}[{index}] must be a non-empty str, got {item!r}")
    return items


def _optional_str(name: str, value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{name} must be null or a non-empty str, got {value!r}")
    return value


@dataclass
class DataConfig:
    """Data pipeline settings. Label: ESTABLISHED.

    See the module docstring for the defaults table.
    """

    sources: list[str] = field(default_factory=list)
    tokenizer_ref: str | None = None

    min_doc_len: int = 1
    max_doc_len: int = 100_000
    language_filter: list[str] = field(default_factory=lambda: ["en"])
    min_quality_score: float = 0.0
    safety_filter: bool = True
    contamination_filter: bool = True

    dedup: bool = True
    dedup_algorithm: str = "minhash"
    dedup_threshold: float = 0.8

    shard_size: int = 100_000
    packing_length: int = 512
    max_tokens: int | None = None
    max_documents: int | None = None
    cache_dir: str | None = None
    drop_remainder: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Re-run every range/shape check.

        Raises
        ------
        ConfigError
            On a bad value or a contradictory pair (e.g. ``min_doc_len`` >
            ``max_doc_len``).
        """
        self.sources = _require_str_list("sources", self.sources)
        self.tokenizer_ref = _optional_str("tokenizer_ref", self.tokenizer_ref)

        _require_int("min_doc_len", self.min_doc_len, minimum=1)
        _require_int("max_doc_len", self.max_doc_len, minimum=1)
        if self.max_doc_len < self.min_doc_len:
            raise ConfigError(
                f"max_doc_len ({self.max_doc_len}) must be >= min_doc_len "
                f"({self.min_doc_len})"
            )

        self.language_filter = _require_str_list("language_filter", self.language_filter)

        quality = _require_float("min_quality_score", self.min_quality_score)
        if not 0.0 <= quality <= 1.0:
            raise ConfigError(f"min_quality_score must be in [0, 1], got {quality}")
        _require_bool("safety_filter", self.safety_filter)
        _require_bool("contamination_filter", self.contamination_filter)

        _require_bool("dedup", self.dedup)
        _require_choice("dedup_algorithm", self.dedup_algorithm, DEDUP_ALGORITHMS)
        threshold = _require_float("dedup_threshold", self.dedup_threshold)
        if not 0.0 <= threshold <= 1.0:
            raise ConfigError(f"dedup_threshold must be in [0, 1], got {threshold}")

        _require_int("shard_size", self.shard_size, minimum=1)
        _require_int("packing_length", self.packing_length, minimum=1)
        if self.max_tokens is not None:
            _require_int("max_tokens", self.max_tokens, minimum=1)
        if self.max_documents is not None:
            _require_int("max_documents", self.max_documents, minimum=1)
        self.cache_dir = _optional_str("cache_dir", self.cache_dir)
        _require_bool("drop_remainder", self.drop_remainder)

    def to_dict(self) -> dict[str, Any]:
        """Config → nested plain ``dict`` (the inverse of :meth:`from_dict`)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> DataConfig:
        """Dict → :class:`DataConfig`; unknown keys raise :class:`ConfigError`."""
        if not isinstance(data, Mapping):
            raise ConfigError(f"DataConfig expects a mapping, got {type(data).__name__}")
        payload = _reject_unknown("DataConfig", data, set(cls.__dataclass_fields__))
        try:
            return cls(**payload)
        except TypeError as exc:
            raise ConfigError(f"invalid DataConfig: {exc}") from exc

    @classmethod
    def from_yaml(cls, path: str | Path) -> DataConfig:
        """YAML file → :class:`DataConfig`.

        Raises :class:`ConfigError` if the file is missing, empty, not a mapping,
        or fails validation.
        """
        file_path = Path(path)
        if not file_path.is_file():
            raise ConfigError(f"data config file not found: {file_path}")
        with file_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if data is None:
            raise ConfigError(f"data config file is empty: {file_path}")
        if not isinstance(data, Mapping):
            raise ConfigError(
                f"data config file must contain a YAML mapping, got "
                f"{type(data).__name__}: {file_path}"
            )
        return cls.from_dict(data)


__all__ = ["DEDUP_ALGORITHMS", "DataConfig", "ConfigError"]
