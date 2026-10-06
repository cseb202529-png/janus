"""Model configuration: dataclasses loaded from YAML, with validation.

- **Label:** ESTABLISHED
- **Phase:** 02
- **Config flag:** the eleven component flags below are the ablation switches
  (``docs/specification.md`` §4); every experimental component defaults to ``False``.

Purpose
-------
Describe a Janus model entirely in YAML, validate it early (fail before a single
tensor is allocated), and round-trip it back to a plain dict for hashing/checkpoints.

Interface
---------
``ModelConfig(vocab_size=..., ...)``
    Validates itself in ``__post_init__``.
``ModelConfig.from_yaml(path) -> ModelConfig``   YAML file → config
``ModelConfig.from_dict(data) -> ModelConfig``   dict → config (unknown keys rejected)
``config.to_dict() -> dict``                     config → plain nested dict
``config.validate() -> None``                    re-run validation (raises ``ConfigError``)

Sub-configs: :class:`MoEConfig`, :class:`SSMConfig`, :class:`TRMConfig`,
:class:`MemoryConfig` (each with its own ``validate``/``to_dict``/``from_dict``).

Tensor shapes: **none** — this module builds no tensors.

Defaults (documented, must match ``tests/unit/config/test_model_config.py``)
---------------------------------------------------------------------------
===================  =========================  ==========================
Field                Default                    Valid range
===================  =========================  ==========================
``vocab_size``       *(required)*               int >= 2
``d_model``          ``768``                    int >= 1
``n_layers``         ``12``                     int >= 1
``n_heads``          ``12``                     int >= 1, divides ``d_model``
``n_kv_heads``       ``None`` → ``n_heads``     int >= 1, divides ``n_heads``
``ffn_dim``          ``None`` → ``4*d_model``   int >= 1
``max_seq_len``      ``512``                    int >= 1
``dropout``          ``0.0``                    float in ``[0, 1)``
``rope_theta``       ``10000.0``                float > 0
``rmsnorm_eps``      ``1e-6``                   float > 0
``tie_embeddings``   ``True``                   bool
``attention``        ``True``                   bool (only non-default flag)
``gqa, mla, ssm, moe, meta_tokens, adaptive_routing,
thought_engine, trm, memory, verifier``         ``False`` each
``n_meta_tokens``    ``0``                      int >= 0; >0 iff ``meta_tokens``
===================  =========================  ==========================

Notes / edge cases / risks
--------------------------
* ``ConfigError`` (a ``ValueError``) is defined here and reused by the other
  ``janus.config`` modules.
* Unknown keys are rejected — a typo must not silently become a default.
* Conflicts raise instead of combining silently (``AGENTS.md`` §3.13):
  ``gqa + mla``, and ``memory`` without ``memory_config.db_path``.
* Bool is rejected where an int is expected (``True`` is an ``int`` in Python).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any, Mapping

import yaml


class ConfigError(ValueError):
    """Raised when a config is invalid, unknown, or contradictory.

    Message always states what is wrong *and* what to set instead.
    """


# ---------------------------------------------------------------------------
# helpers (private to this module; duplicated minimally in the sibling configs
# so that no unspecced module has to be created)
# ---------------------------------------------------------------------------
def _require_int(name: str, value: Any, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigError(f"{name} must be an int, got {type(value).__name__}: {value!r}")
    if value < minimum:
        raise ConfigError(f"{name} must be >= {minimum}, got {value}")
    return value


def _require_float(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError(f"{name} must be a number, got {type(value).__name__}: {value!r}")
    value = float(value)
    if value != value or value in (float("inf"), float("-inf")):
        raise ConfigError(f"{name} must be finite, got {value!r}")
    return value


def _require_bool(name: str, value: Any) -> bool:
    if not isinstance(value, bool):
        raise ConfigError(f"{name} must be a bool, got {type(value).__name__}: {value!r}")
    return value


def _require_choice(name: str, value: Any, choices: tuple[str, ...]) -> str:
    if not isinstance(value, str) or value not in choices:
        raise ConfigError(f"{name} must be one of {choices}, got {value!r}")
    return value


def _reject_unknown(cls_name: str, data: Mapping[str, Any], valid: set[str]) -> dict[str, Any]:
    unknown = sorted(set(data) - valid)
    if unknown:
        raise ConfigError(
            f"unknown {cls_name} key(s): {unknown}; valid keys: {sorted(valid)}"
        )
    return dict(data)


# ---------------------------------------------------------------------------
# sub-configs
# ---------------------------------------------------------------------------
@dataclass
class MoEConfig:
    """Mixture-of-Experts FFN settings. Label: ESTABLISHED (Phase 13).

    ==================  ==============  ============================
    Field               Default         Valid range
    ==================  ==============  ============================
    ``n_experts``       ``4``           int >= 2
    ``top_k``           ``2``           int, 1 <= k <= n_experts
    ``capacity_factor`` ``1.25``        float > 0
    ``load_balance_weight`` ``0.01``    float in [0, 1]
    ``expert_ffn_dim``  ``None``        None, or int >= 1
    ==================  ==============  ============================
    """

    n_experts: int = 4
    top_k: int = 2
    capacity_factor: float = 1.25
    load_balance_weight: float = 0.01
    expert_ffn_dim: int | None = None

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Raise :class:`ConfigError` if any MoE field is out of range."""
        _require_int("moe.n_experts", self.n_experts, minimum=2)
        _require_int("moe.top_k", self.top_k, minimum=1)
        if self.top_k > self.n_experts:
            raise ConfigError(
                f"moe.top_k ({self.top_k}) must be <= moe.n_experts ({self.n_experts})"
            )
        capacity = _require_float("moe.capacity_factor", self.capacity_factor)
        if capacity <= 0:
            raise ConfigError(f"moe.capacity_factor must be > 0, got {capacity}")
        weight = _require_float("moe.load_balance_weight", self.load_balance_weight)
        if not 0.0 <= weight <= 1.0:
            raise ConfigError(f"moe.load_balance_weight must be in [0, 1], got {weight}")
        if self.expert_ffn_dim is not None:
            _require_int("moe.expert_ffn_dim", self.expert_ffn_dim, minimum=1)

    def to_dict(self) -> dict[str, Any]:
        """Output: plain ``dict`` of this sub-config."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> MoEConfig:
        """Dict → :class:`MoEConfig`; unknown keys raise :class:`ConfigError`."""
        if not isinstance(data, Mapping):
            raise ConfigError(f"moe_config must be a mapping, got {type(data).__name__}")
        payload = _reject_unknown("MoEConfig", data, set(cls.__dataclass_fields__))
        try:
            return cls(**payload)
        except TypeError as exc:
            raise ConfigError(f"invalid moe_config: {exc}") from exc


@dataclass
class SSMConfig:
    """State-space (Mamba-style) block settings. Label: ESTABLISHED (Phase 10).

    ==================  ==============  ============================
    Field               Default         Valid range
    ==================  ==============  ============================
    ``state_dim``       ``16``          int >= 1  (N)
    ``expand``          ``2``           int >= 1
    ``conv_kernel``     ``4``           int >= 1  (padding chosen in ssm.py)
    ``dt_rank``         ``"auto"``      ``"auto"`` or int >= 1
    ``dt_min``          ``1e-3``        float, 0 < dt_min < dt_max
    ``dt_max``          ``1e-1``        float, 0 < dt_min < dt_max
    ==================  ==============  ============================
    """

    state_dim: int = 16
    expand: int = 2
    conv_kernel: int = 4
    dt_rank: int | str = "auto"
    dt_min: float = 1e-3
    dt_max: float = 1e-1

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Raise :class:`ConfigError` if any SSM field is out of range."""
        _require_int("ssm.state_dim", self.state_dim, minimum=1)
        _require_int("ssm.expand", self.expand, minimum=1)
        _require_int("ssm.conv_kernel", self.conv_kernel, minimum=1)
        if self.dt_rank != "auto":
            _require_int("ssm.dt_rank", self.dt_rank, minimum=1)
        dt_min = _require_float("ssm.dt_min", self.dt_min)
        dt_max = _require_float("ssm.dt_max", self.dt_max)
        if dt_min <= 0 or dt_max <= 0:
            raise ConfigError(f"ssm.dt_min/dt_max must be > 0, got {dt_min}/{dt_max}")
        if dt_min >= dt_max:
            raise ConfigError(f"ssm.dt_min ({dt_min}) must be < ssm.dt_max ({dt_max})")

    def to_dict(self) -> dict[str, Any]:
        """Output: plain ``dict`` of this sub-config."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SSMConfig:
        """Dict → :class:`SSMConfig`; unknown keys raise :class:`ConfigError`."""
        if not isinstance(data, Mapping):
            raise ConfigError(f"ssm_config must be a mapping, got {type(data).__name__}")
        payload = _reject_unknown("SSMConfig", data, set(cls.__dataclass_fields__))
        try:
            return cls(**payload)
        except TypeError as exc:
            raise ConfigError(f"invalid ssm_config: {exc}") from exc


@dataclass
class TRMConfig:
    """Test-time recursive refinement loop settings. Label: EXPERIMENTAL (Phase 16).

    ======================  ==============  ============================
    Field                   Default         Valid range
    ======================  ==============  ============================
    ``max_steps``           ``4``           int >= 1
    ``min_steps``           ``1``           int, 1 <= min <= max
    ``halt_threshold``      ``0.5``         float in (0, 1)
    ``verifier_gated``      ``True``        bool
    ``hidden_dim``          ``None``        None (→ d_model), or int >= 1
    ======================  ==============  ============================
    """

    max_steps: int = 4
    min_steps: int = 1
    halt_threshold: float = 0.5
    verifier_gated: bool = True
    hidden_dim: int | None = None

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Raise :class:`ConfigError` if any TRM field is out of range."""
        _require_int("trm.max_steps", self.max_steps, minimum=1)
        _require_int("trm.min_steps", self.min_steps, minimum=1)
        if self.min_steps > self.max_steps:
            raise ConfigError(
                f"trm.min_steps ({self.min_steps}) must be <= trm.max_steps ({self.max_steps})"
            )
        threshold = _require_float("trm.halt_threshold", self.halt_threshold)
        if not 0.0 < threshold < 1.0:
            raise ConfigError(f"trm.halt_threshold must be in (0, 1), got {threshold}")
        _require_bool("trm.verifier_gated", self.verifier_gated)
        if self.hidden_dim is not None:
            _require_int("trm.hidden_dim", self.hidden_dim, minimum=1)

    def to_dict(self) -> dict[str, Any]:
        """Output: plain ``dict`` of this sub-config."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> TRMConfig:
        """Dict → :class:`TRMConfig`; unknown keys raise :class:`ConfigError`."""
        if not isinstance(data, Mapping):
            raise ConfigError(f"trm_config must be a mapping, got {type(data).__name__}")
        payload = _reject_unknown("TRMConfig", data, set(cls.__dataclass_fields__))
        try:
            return cls(**payload)
        except TypeError as exc:
            raise ConfigError(f"invalid trm_config: {exc}") from exc


@dataclass
class MemoryConfig:
    """External SQLite memory settings. Label: EXPERIMENTAL (Phase 17).

    ====================  ==============  ============================
    Field                 Default         Valid range
    ====================  ==============  ============================
    ``db_path``           ``None``        None, or a non-empty str path
    ``top_k``             ``3``           int >= 1
    ``embedding_dim``     ``None``        None (→ d_model), or int >= 1
    ``write_enabled``     ``True``        bool
    ``max_entries``       ``100000``      int >= 1
    ====================  ==============  ============================

    ``db_path`` has **no** default on purpose: no path is hard-coded anywhere
    (``AGENTS.md`` §3.7). Enabling ``memory: true`` without setting
    ``memory_config.db_path`` in YAML raises :class:`ConfigError`.
    """

    db_path: str | None = None
    top_k: int = 3
    embedding_dim: int | None = None
    write_enabled: bool = True
    max_entries: int = 100_000

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Raise :class:`ConfigError` if any memory field is out of range."""
        if self.db_path is not None:
            if not isinstance(self.db_path, str) or not self.db_path.strip():
                raise ConfigError(
                    "memory.db_path must be a non-empty str (or null when memory is off), "
                    f"got {self.db_path!r}"
                )
        _require_int("memory.top_k", self.top_k, minimum=1)
        if self.embedding_dim is not None:
            _require_int("memory.embedding_dim", self.embedding_dim, minimum=1)
        _require_bool("memory.write_enabled", self.write_enabled)
        _require_int("memory.max_entries", self.max_entries, minimum=1)

    def to_dict(self) -> dict[str, Any]:
        """Output: plain ``dict`` of this sub-config."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> MemoryConfig:
        """Dict → :class:`MemoryConfig`; unknown keys raise :class:`ConfigError`."""
        if not isinstance(data, Mapping):
            raise ConfigError(f"memory_config must be a mapping, got {type(data).__name__}")
        payload = _reject_unknown("MemoryConfig", data, set(cls.__dataclass_fields__))
        try:
            return cls(**payload)
        except TypeError as exc:
            raise ConfigError(f"invalid memory_config: {exc}") from exc


# ---------------------------------------------------------------------------
# the model config itself
# ---------------------------------------------------------------------------
#: Component flags from ``docs/ARCHITECTURE.md`` — the ablation switches.
COMPONENT_FLAGS: tuple[str, ...] = (
    "attention",
    "gqa",
    "mla",
    "ssm",
    "moe",
    "meta_tokens",
    "adaptive_routing",
    "thought_engine",
    "trm",
    "memory",
    "verifier",
)

_NESTED_KEYS: dict[str, type] = {
    "moe_config": MoEConfig,
    "ssm_config": SSMConfig,
    "trm_config": TRMConfig,
    "memory_config": MemoryConfig,
}


@dataclass
class ModelConfig:
    """Full description of a Janus model. Label: ESTABLISHED.

    See the module docstring for the defaults table. All component flags default
    to ``False`` except ``attention`` (the baseline backbone piece).
    """

    vocab_size: int

    # core dimensions
    d_model: int = 768
    n_layers: int = 12
    n_heads: int = 12
    n_kv_heads: int | None = None
    ffn_dim: int | None = None
    max_seq_len: int = 512

    # numerics / regularisation
    dropout: float = 0.0
    rope_theta: float = 10000.0
    rmsnorm_eps: float = 1e-6
    tie_embeddings: bool = True

    # component flags (ablation switches)
    attention: bool = True
    gqa: bool = False
    mla: bool = False
    ssm: bool = False
    moe: bool = False
    meta_tokens: bool = False
    adaptive_routing: bool = False
    thought_engine: bool = False
    trm: bool = False
    memory: bool = False
    verifier: bool = False

    # meta-token budget (only meaningful when meta_tokens is True)
    n_meta_tokens: int = 0

    # sub-configs
    moe_config: MoEConfig = field(default_factory=MoEConfig)
    ssm_config: SSMConfig = field(default_factory=SSMConfig)
    trm_config: TRMConfig = field(default_factory=TRMConfig)
    memory_config: MemoryConfig = field(default_factory=MemoryConfig)

    def __post_init__(self) -> None:
        self._normalise()
        self.validate()

    # -- derived, documented defaults + sub-config coercion ----------------
    def _normalise(self) -> None:
        """Fill ``None`` placeholders with their documented derivations and
        coerce nested sub-configs given as plain mappings.

        So ``ModelConfig(vocab_size=..., moe_config={"n_experts": 2})`` behaves
        exactly like ``ModelConfig.from_dict(...)``.
        """
        if self.n_kv_heads is None:
            self.n_kv_heads = self.n_heads
        if self.ffn_dim is None:
            self.ffn_dim = 4 * self.d_model
        for key, klass in _NESTED_KEYS.items():
            raw = getattr(self, key)
            if raw is None:
                setattr(self, key, klass())
            elif isinstance(raw, klass):
                continue
            elif isinstance(raw, Mapping):
                setattr(self, key, klass.from_dict(raw))
            else:
                raise ConfigError(
                    f"{key} must be a mapping or {klass.__name__}, "
                    f"got {type(raw).__name__}"
                )

    # -- derived properties ----------------------------------------------
    @property
    def head_dim(self) -> int:
        """Output: ``int`` = ``d_model // n_heads`` (validated as exact)."""
        return self.d_model // self.n_heads

    @property
    def text_budget(self) -> int:
        """Output: ``int`` — max *text* tokens: ``max_seq_len - n_meta_tokens``.

        Meta tokens occupy positions ``0..n_meta_tokens-1`` (watchlist item 5).
        """
        return self.max_seq_len - self.n_meta_tokens

    def component_flags(self) -> dict[str, bool]:
        """Output: ``dict[str, bool]`` of the eleven :data:`COMPONENT_FLAGS`."""
        return {name: bool(getattr(self, name)) for name in COMPONENT_FLAGS}

    # -- validation --------------------------------------------------------
    def validate(self) -> None:
        """Re-run every validation rule.

        Raises
        ------
        ConfigError
            On a bad value, a violated cross-field rule, or a component conflict.
        """
        _require_int("vocab_size", self.vocab_size, minimum=2)
        _require_int("d_model", self.d_model, minimum=1)
        _require_int("n_layers", self.n_layers, minimum=1)
        _require_int("n_heads", self.n_heads, minimum=1)
        _require_int("ffn_dim", self.ffn_dim, minimum=1)  # resolved in __post_init__
        _require_int("max_seq_len", self.max_seq_len, minimum=1)
        _require_int("n_kv_heads", self.n_kv_heads, minimum=1)  # resolved too

        if self.d_model % self.n_heads != 0:
            raise ConfigError(
                f"n_heads ({self.n_heads}) must divide d_model ({self.d_model}); "
                f"choose d_model as a multiple of n_heads"
            )
        if self.n_kv_heads > self.n_heads:
            raise ConfigError(
                f"n_kv_heads ({self.n_kv_heads}) must be <= n_heads ({self.n_heads})"
            )
        if self.n_heads % self.n_kv_heads != 0:
            raise ConfigError(
                f"n_kv_heads ({self.n_kv_heads}) must divide n_heads ({self.n_heads})"
            )

        dropout = _require_float("dropout", self.dropout)
        if not 0.0 <= dropout < 1.0:
            raise ConfigError(f"dropout must be in [0, 1), got {dropout}")
        if _require_float("rope_theta", self.rope_theta) <= 0:
            raise ConfigError(f"rope_theta must be > 0, got {self.rope_theta}")
        if _require_float("rmsnorm_eps", self.rmsnorm_eps) <= 0:
            raise ConfigError(f"rmsnorm_eps must be > 0, got {self.rmsnorm_eps}")
        _require_int("n_meta_tokens", self.n_meta_tokens, minimum=0)

        for name in COMPONENT_FLAGS:
            _require_bool(name, getattr(self, name))
        _require_bool("tie_embeddings", self.tie_embeddings)

        # -- component conflicts (AGENTS.md §3.13: never combine silently) --
        if self.gqa and self.mla:
            raise ConfigError(
                "gqa and mla are mutually exclusive alternatives for the KV path; "
                "run them as separate experiment variants (docs/DECISIONS.md)"
            )
        if (self.gqa or self.mla) and not self.attention:
            raise ConfigError(
                "gqa/mla require the attention path: set attention: true "
                "(or disable gqa/mla)"
            )
        if not self.attention and not self.ssm:
            raise ConfigError(
                "backbone needs a block type: enable attention and/or ssm"
            )
        if self.gqa and self.n_kv_heads >= self.n_heads:
            raise ConfigError(
                f"gqa: true requires n_kv_heads ({self.n_kv_heads}) < n_heads "
                f"({self.n_heads}); set n_kv_heads or disable gqa"
            )
        if self.ssm and self.n_layers < 2:
            raise ConfigError(
                f"ssm: true with n_layers={self.n_layers} cannot alternate A/S blocks; "
                "set n_layers >= 2 or disable ssm"
            )

        # -- meta tokens ---------------------------------------------------
        if self.meta_tokens:
            if self.n_meta_tokens < 1:
                raise ConfigError(
                    "meta_tokens: true requires n_meta_tokens >= 1 "
                    "(meta tokens occupy positions 0..n_meta_tokens-1)"
                )
            if self.n_meta_tokens >= self.max_seq_len:
                raise ConfigError(
                    f"n_meta_tokens ({self.n_meta_tokens}) must be < max_seq_len "
                    f"({self.max_seq_len}) so at least one text token fits"
                )
        elif self.n_meta_tokens != 0:
            raise ConfigError(
                f"n_meta_tokens is {self.n_meta_tokens} but meta_tokens is false; "
                "set meta_tokens: true or n_meta_tokens: 0 (no silent no-op)"
            )

        # -- sub-configs ---------------------------------------------------
        self.moe_config.validate()
        self.ssm_config.validate()
        self.trm_config.validate()
        self.memory_config.validate()

        if self.memory and not (
            isinstance(self.memory_config.db_path, str) and self.memory_config.db_path.strip()
        ):
            raise ConfigError(
                "memory: true requires memory_config.db_path (no path is hard-coded); "
                "set it in the YAML config"
            )

    # -- (de)serialisation -------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        """Config → nested plain ``dict`` (JSON/YAML-safe; the inverse of ``from_dict``)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ModelConfig:
        """Dict → :class:`ModelConfig`.

        Raises :class:`ConfigError` on a non-mapping input, unknown keys, a
        malformed sub-config, or any validation failure.
        """
        if not isinstance(data, Mapping):
            raise ConfigError(f"ModelConfig expects a mapping, got {type(data).__name__}")

        valid = set(cls.__dataclass_fields__)
        payload = _reject_unknown("ModelConfig", data, valid)

        for key, klass in _NESTED_KEYS.items():
            if key not in payload:
                continue
            raw = payload[key]
            if raw is None:
                payload[key] = klass()
            elif isinstance(raw, klass):
                continue
            elif isinstance(raw, Mapping):
                payload[key] = klass.from_dict(raw)
            else:
                raise ConfigError(
                    f"{key} must be a mapping or {klass.__name__}, got {type(raw).__name__}"
                )

        try:
            return cls(**payload)
        except TypeError as exc:
            raise ConfigError(f"invalid ModelConfig: {exc}") from exc

    @classmethod
    def from_yaml(cls, path: str | Path) -> ModelConfig:
        """YAML file → :class:`ModelConfig`.

        Raises :class:`ConfigError` if the file is missing, empty, not a mapping,
        or fails validation.
        """
        file_path = Path(path)
        if not file_path.is_file():
            raise ConfigError(f"model config file not found: {file_path}")
        with file_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if data is None:
            raise ConfigError(f"model config file is empty: {file_path}")
        if not isinstance(data, Mapping):
            raise ConfigError(
                f"model config file must contain a YAML mapping, got "
                f"{type(data).__name__}: {file_path}"
            )
        return cls.from_dict(data)


__all__ = [
    "ConfigError",
    "COMPONENT_FLAGS",
    "MoEConfig",
    "SSMConfig",
    "TRMConfig",
    "MemoryConfig",
    "ModelConfig",
]
