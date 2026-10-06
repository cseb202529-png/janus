"""Training hyperparameter configuration loaded from YAML, with validation.

- **Label:** ESTABLISHED
- **Phase:** 02
- **Config flag:** none (this *is* the config layer); ``precision`` and ``device``
  are resolved at runtime by ``utils.device`` instead of being hard-coded.

Purpose
-------
Hold every optimisation knob the trainer reads, validate ranges up front, and
round-trip to a plain dict for hashing and checkpoint metadata.

Interface
---------
``TrainingConfig(...)``            validates itself in ``__post_init__``
``TrainingConfig.from_yaml(path)`` YAML → config
``TrainingConfig.from_dict(data)`` dict → config (unknown keys rejected)
``config.to_dict() -> dict``       config → nested plain dict
``config.validate() -> None``      re-run validation (raises ``ConfigError``)

Tensor shapes: **none** — no tensors are created here.

Defaults (documented; asserted in ``tests/unit/config/test_training_config.py``)
-------------------------------------------------------------------------------
=========================  ==================  ==========================
Field                      Default             Valid range
=========================  ==================  ==========================
``optimizer``              ``"adamw"``         one of adamw|adam|sgd
``lr``                     ``3.0e-4``          float in (0, 1]
``min_lr``                 ``1.0e-5``          float in [0, lr]
``weight_decay``           ``0.1``             float in [0, 1]
``beta1``                  ``0.9``             float in [0, 1)
``beta2``                  ``0.95``            float in [0, 1)
``eps``                    ``1.0e-8``          float > 0
``warmup_steps``           ``1000``            int >= 0
``total_steps``            ``100000``          int >= 1, > warmup_steps
``schedule``               ``"cosine"``        one of cosine|linear|constant
``grad_clip``              ``1.0``             float >= 0 (0 disables)
``precision``              ``"auto"``          one of auto|fp32|fp16|bf16
``grad_accum_steps``       ``1``               int >= 1
``batch_size``             ``8``               int >= 1
``eval_interval``          ``500``             int >= 1
``log_interval``           ``50``              int >= 1
``checkpoint_interval``    ``1000``            int >= 1
``keep_last_checkpoints``  ``3``               int >= 1
``seed``                   ``1337``            int >= 0
``device``                 ``"auto"``          auto|cpu|cuda|mps
``num_workers``            ``0``               int >= 0
``resume_from``            ``None``            None, or non-empty path str
``deterministic``          ``False``           bool
=========================  ==================  ==========================

Notes / edge cases / risks
--------------------------
* No device, CUDA id or path is hard-coded: ``device`` defaults to ``"auto"``
  and ``resume_from`` defaults to ``null``.
* ``total_steps > warmup_steps`` is enforced so the LR schedule never divides by zero.
* ``seed`` allows any non-negative int (negative seeds raise).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
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

OPTIMIZERS: tuple[str, ...] = ("adamw", "adam", "sgd")
SCHEDULES: tuple[str, ...] = ("cosine", "linear", "constant")
PRECISIONS: tuple[str, ...] = ("auto", "fp32", "fp16", "bf16")
DEVICES: tuple[str, ...] = ("auto", "cpu", "cuda", "mps")


@dataclass
class TrainingConfig:
    """Optimisation hyperparameters. Label: ESTABLISHED.

    See the module docstring for the defaults table.
    """

    optimizer: str = "adamw"
    lr: float = 3.0e-4
    min_lr: float = 1.0e-5
    weight_decay: float = 0.1
    beta1: float = 0.9
    beta2: float = 0.95
    eps: float = 1.0e-8

    warmup_steps: int = 1000
    total_steps: int = 100_000
    schedule: str = "cosine"

    grad_clip: float = 1.0
    precision: str = "auto"
    grad_accum_steps: int = 1
    batch_size: int = 8

    eval_interval: int = 500
    log_interval: int = 50
    checkpoint_interval: int = 1000
    keep_last_checkpoints: int = 3

    seed: int = 1337
    device: str = "auto"
    num_workers: int = 0
    resume_from: str | None = None
    deterministic: bool = False

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Re-run every range check.

        Raises
        ------
        ConfigError
            On an out-of-range value, an unknown choice, or a contradictory pair.
        """
        _require_choice("optimizer", self.optimizer, OPTIMIZERS)
        _require_choice("schedule", self.schedule, SCHEDULES)
        _require_choice("precision", self.precision, PRECISIONS)
        _require_choice("device", self.device, DEVICES)

        lr = _require_float("lr", self.lr)
        if not 0.0 < lr <= 1.0:
            raise ConfigError(f"lr must be in (0, 1], got {lr}")
        min_lr = _require_float("min_lr", self.min_lr)
        if min_lr < 0.0:
            raise ConfigError(f"min_lr must be >= 0, got {min_lr}")
        if min_lr > lr:
            raise ConfigError(f"min_lr ({min_lr}) must be <= lr ({lr})")

        weight_decay = _require_float("weight_decay", self.weight_decay)
        if not 0.0 <= weight_decay <= 1.0:
            raise ConfigError(f"weight_decay must be in [0, 1], got {weight_decay}")

        beta1 = _require_float("beta1", self.beta1)
        beta2 = _require_float("beta2", self.beta2)
        for name, value in (("beta1", beta1), ("beta2", beta2)):
            if not 0.0 <= value < 1.0:
                raise ConfigError(f"{name} must be in [0, 1), got {value}")
        if _require_float("eps", self.eps) <= 0:
            raise ConfigError(f"eps must be > 0, got {self.eps}")

        _require_int("warmup_steps", self.warmup_steps, minimum=0)
        _require_int("total_steps", self.total_steps, minimum=1)
        if self.total_steps <= self.warmup_steps:
            raise ConfigError(
                f"total_steps ({self.total_steps}) must be > warmup_steps "
                f"({self.warmup_steps})"
            )

        grad_clip = _require_float("grad_clip", self.grad_clip)
        if grad_clip < 0:
            raise ConfigError(f"grad_clip must be >= 0 (0 disables clipping), got {grad_clip}")

        _require_int("grad_accum_steps", self.grad_accum_steps, minimum=1)
        _require_int("batch_size", self.batch_size, minimum=1)
        _require_int("eval_interval", self.eval_interval, minimum=1)
        _require_int("log_interval", self.log_interval, minimum=1)
        _require_int("checkpoint_interval", self.checkpoint_interval, minimum=1)
        _require_int("keep_last_checkpoints", self.keep_last_checkpoints, minimum=1)
        _require_int("seed", self.seed, minimum=0)
        _require_int("num_workers", self.num_workers, minimum=0)

        if self.resume_from is not None and (
            not isinstance(self.resume_from, str) or not self.resume_from.strip()
        ):
            raise ConfigError(
                f"resume_from must be null or a non-empty path str, got {self.resume_from!r}"
            )
        _require_bool("deterministic", self.deterministic)

    def to_dict(self) -> dict[str, Any]:
        """Config → nested plain ``dict`` (the inverse of :meth:`from_dict`)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> TrainingConfig:
        """Dict → :class:`TrainingConfig`; unknown keys raise :class:`ConfigError`."""
        if not isinstance(data, Mapping):
            raise ConfigError(f"TrainingConfig expects a mapping, got {type(data).__name__}")
        payload = _reject_unknown("TrainingConfig", data, set(cls.__dataclass_fields__))
        try:
            return cls(**payload)
        except TypeError as exc:
            raise ConfigError(f"invalid TrainingConfig: {exc}") from exc

    @classmethod
    def from_yaml(cls, path: str | Path) -> TrainingConfig:
        """YAML file → :class:`TrainingConfig`.

        Raises :class:`ConfigError` if the file is missing, empty, not a mapping,
        or fails validation.
        """
        file_path = Path(path)
        if not file_path.is_file():
            raise ConfigError(f"training config file not found: {file_path}")
        with file_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if data is None:
            raise ConfigError(f"training config file is empty: {file_path}")
        if not isinstance(data, Mapping):
            raise ConfigError(
                f"training config file must contain a YAML mapping, got "
                f"{type(data).__name__}: {file_path}"
            )
        return cls.from_dict(data)


__all__ = [
    "OPTIMIZERS",
    "SCHEDULES",
    "PRECISIONS",
    "DEVICES",
    "TrainingConfig",
    "ConfigError",
]
