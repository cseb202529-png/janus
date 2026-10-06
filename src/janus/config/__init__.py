"""YAML-backed configuration for Janus.

- **Label:** ESTABLISHED
- **Phase:** 02

Every hyperparameter lives here (or in YAML loaded here) — nothing is hard-coded
in library code (``AGENTS.md`` §3.7).

Modules
-------
``model_config``      :class:`ModelConfig` + ``MoE/SSM/TRM/MemoryConfig`` (Phase 02)
``training_config``   :class:`TrainingConfig` (Phase 02)
``data_config``       :class:`DataConfig` (Phase 02)
``generation_config`` :class:`GenerationConfig` (Phase 47)

Usage
-----
>>> from janus.config import ModelConfig, ConfigError
>>> cfg = ModelConfig.from_dict({"vocab_size": 256, "d_model": 32, "n_heads": 4})
>>> cfg.head_dim
8

``ConfigError`` (a ``ValueError``) is raised for every invalid or contradictory
config and is shared by all four modules.
"""

from __future__ import annotations

from janus.config.data_config import DEDUP_ALGORITHMS, DataConfig
from janus.config.model_config import (
    COMPONENT_FLAGS,
    ConfigError,
    MemoryConfig,
    MoEConfig,
    ModelConfig,
    SSMConfig,
    TRMConfig,
)
from janus.config.training_config import (
    DEVICES,
    OPTIMIZERS,
    PRECISIONS,
    SCHEDULES,
    TrainingConfig,
)

__all__ = [
    "COMPONENT_FLAGS",
    "ConfigError",
    "MemoryConfig",
    "MoEConfig",
    "ModelConfig",
    "SSMConfig",
    "TRMConfig",
    "TrainingConfig",
    "DataConfig",
    "OPTIMIZERS",
    "SCHEDULES",
    "PRECISIONS",
    "DEVICES",
    "DEDUP_ALGORITHMS",
]
