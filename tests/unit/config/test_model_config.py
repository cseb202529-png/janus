"""Phase 02 tests for `janus/config/model_config.py`.

Required by `src/janus/config/model_config.spec.md`:
load valid YAML; reject invalid (heads not dividing d_model, kv_heads not dividing
heads); round trip to dict; defaults documented. CPU only, tiny configs.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import janus.config.model_config as model_config_module
from janus.config import (
    COMPONENT_FLAGS,
    ConfigError,
    MemoryConfig,
    MoEConfig,
    ModelConfig,
    SSMConfig,
    TRMConfig,
)

TINY = {
    "vocab_size": 256,
    "d_model": 32,
    "n_layers": 2,
    "n_heads": 4,
    "ffn_dim": 64,
    "max_seq_len": 64,
}


def _tiny(**overrides) -> dict:
    data = dict(TINY)
    data.update(overrides)
    return data


# ---------------------------------------------------------------------------
# defaults (documented)
# ---------------------------------------------------------------------------
def test_defaults_documented_in_docstring() -> None:
    """The defaults table must exist in the module docstring (documented defaults)."""
    module_doc = model_config_module.__doc__ or ""
    for token in ("d_model", "``768``", "n_layers", "``12``", "max_seq_len", "``512``"):
        assert token in module_doc, f"defaults table is missing {token!r}"
    assert ModelConfig.__doc__


def test_documented_default_values() -> None:
    cfg = ModelConfig(vocab_size=1000)
    assert cfg.d_model == 768
    assert cfg.n_layers == 12
    assert cfg.n_heads == 12
    assert cfg.n_kv_heads == 12  # None -> n_heads
    assert cfg.ffn_dim == 4 * 768  # None -> 4 * d_model
    assert cfg.max_seq_len == 512
    assert cfg.dropout == 0.0
    assert cfg.rope_theta == 10000.0
    assert cfg.rmsnorm_eps == 1e-6
    assert cfg.tie_embeddings is True
    assert cfg.n_meta_tokens == 0


def test_component_flags_default_false_except_attention() -> None:
    cfg = ModelConfig(vocab_size=1000)
    flags = cfg.component_flags()
    assert set(flags) == set(COMPONENT_FLAGS)
    assert flags["attention"] is True
    for name, value in flags.items():
        if name != "attention":
            assert value is False, f"{name} must default to False, got {value}"


def test_derived_head_dim_and_text_budget() -> None:
    cfg = ModelConfig(**_tiny(n_meta_tokens=0))
    assert cfg.head_dim == cfg.d_model // cfg.n_heads
    assert cfg.text_budget == cfg.max_seq_len

    with_meta = ModelConfig(**_tiny(meta_tokens=True, n_meta_tokens=4))
    assert with_meta.text_budget == cfg.max_seq_len - 4


# ---------------------------------------------------------------------------
# YAML
# ---------------------------------------------------------------------------
def test_load_valid_yaml(tmp_path: Path) -> None:
    path = tmp_path / "model.yaml"
    path.write_text(yaml.safe_dump(_tiny(gqa=True, n_kv_heads=2)), encoding="utf-8")
    cfg = ModelConfig.from_yaml(path)
    assert cfg.vocab_size == 256
    assert cfg.n_kv_heads == 2
    assert cfg.gqa is True


def test_yaml_round_trip(tmp_path: Path) -> None:
    original = ModelConfig(**_tiny(moe=True, moe_config={"n_experts": 2, "top_k": 1}))
    path = tmp_path / "model.yaml"
    path.write_text(yaml.safe_dump(original.to_dict()), encoding="utf-8")
    assert ModelConfig.from_yaml(path) == original


def test_yaml_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not found"):
        ModelConfig.from_yaml(tmp_path / "nope.yaml")


def test_yaml_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")
    with pytest.raises(ConfigError, match="empty"):
        ModelConfig.from_yaml(path)


def test_yaml_not_a_mapping(tmp_path: Path) -> None:
    path = tmp_path / "list.yaml"
    path.write_text("- 1\n- 2\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="mapping"):
        ModelConfig.from_yaml(path)


def test_yaml_invalid_value_reports_config_error(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(yaml.safe_dump(_tiny(n_heads=3)), encoding="utf-8")
    with pytest.raises(ConfigError, match="divide"):
        ModelConfig.from_yaml(path)


# ---------------------------------------------------------------------------
# rejection of invalid configs
# ---------------------------------------------------------------------------
def test_reject_heads_not_dividing_d_model() -> None:
    with pytest.raises(ConfigError, match="n_heads .* must divide d_model"):
        ModelConfig(**_tiny(n_heads=5))  # 32 % 5 != 0


def test_reject_kv_heads_not_dividing_heads() -> None:
    with pytest.raises(ConfigError, match="n_kv_heads .* must divide n_heads"):
        ModelConfig(**_tiny(n_kv_heads=3, gqa=True))  # 4 % 3 != 0


def test_reject_kv_heads_greater_than_heads() -> None:
    with pytest.raises(ConfigError, match="must be <= n_heads"):
        ModelConfig(**_tiny(n_kv_heads=8, gqa=True))


def test_reject_gqa_without_fewer_kv_heads() -> None:
    with pytest.raises(ConfigError, match="requires n_kv_heads"):
        ModelConfig(**_tiny(gqa=True, n_kv_heads=4))  # equals n_heads


def test_reject_gqa_and_mla_together() -> None:
    """AGENTS.md §3.13: conflicting techniques must not combine silently."""
    with pytest.raises(ConfigError, match="mutually exclusive"):
        ModelConfig(**_tiny(gqa=True, mla=True, n_kv_heads=2))


def test_reject_mla_without_attention() -> None:
    with pytest.raises(ConfigError, match="require the attention path"):
        ModelConfig(**_tiny(attention=False, mla=True, ssm=True))


def test_reject_backbone_with_no_block_type() -> None:
    with pytest.raises(ConfigError, match="backbone needs a block type"):
        ModelConfig(**_tiny(attention=False, ssm=False))


def test_reject_ssm_with_single_layer() -> None:
    with pytest.raises(ConfigError, match="n_layers >= 2"):
        ModelConfig(**_tiny(n_layers=1, ssm=True))


def test_reject_unknown_key() -> None:
    with pytest.raises(ConfigError, match="unknown ModelConfig key"):
        ModelConfig.from_dict(_tiny(d_modelz=32))


def test_reject_bad_value_types() -> None:
    with pytest.raises(ConfigError, match="d_model must be an int"):
        ModelConfig.from_dict(_tiny(d_model="32"))
    with pytest.raises(ConfigError, match="d_model must be an int"):
        ModelConfig.from_dict(_tiny(d_model=True))  # bool is an int: rejected


def test_reject_vocab_size_too_small() -> None:
    with pytest.raises(ConfigError, match="vocab_size must be >= 2"):
        ModelConfig.from_dict(_tiny(vocab_size=1))


def test_reject_zero_layers() -> None:
    with pytest.raises(ConfigError, match="n_layers must be >= 1"):
        ModelConfig.from_dict(_tiny(n_layers=0))


def test_reject_dropout_out_of_range() -> None:
    with pytest.raises(ConfigError, match="dropout must be in"):
        ModelConfig.from_dict(_tiny(dropout=1.0))
    with pytest.raises(ConfigError, match="dropout must be in"):
        ModelConfig.from_dict(_tiny(dropout=-0.1))


def test_reject_non_finite_rope_theta() -> None:
    with pytest.raises(ConfigError, match="rope_theta must be finite"):
        ModelConfig.from_dict(_tiny(rope_theta=float("nan")))


def test_reject_non_positive_rmsnorm_eps() -> None:
    with pytest.raises(ConfigError, match="rmsnorm_eps must be > 0"):
        ModelConfig.from_dict(_tiny(rmsnorm_eps=0.0))


# ---------------------------------------------------------------------------
# meta tokens
# ---------------------------------------------------------------------------
def test_reject_meta_tokens_without_count() -> None:
    with pytest.raises(ConfigError, match="requires n_meta_tokens >= 1"):
        ModelConfig(**_tiny(meta_tokens=True, n_meta_tokens=0))


def test_reject_meta_tokens_count_without_flag() -> None:
    with pytest.raises(ConfigError, match="no silent no-op"):
        ModelConfig(**_tiny(meta_tokens=False, n_meta_tokens=4))


def test_reject_meta_tokens_filling_context() -> None:
    with pytest.raises(ConfigError, match="must be < max_seq_len"):
        ModelConfig(**_tiny(meta_tokens=True, n_meta_tokens=64, max_seq_len=64))


# ---------------------------------------------------------------------------
# sub-configs
# ---------------------------------------------------------------------------
def test_memory_flag_requires_db_path() -> None:
    with pytest.raises(ConfigError, match="db_path"):
        ModelConfig(**_tiny(memory=True))


def test_memory_flag_with_db_path_ok(tmp_path: Path) -> None:
    cfg = ModelConfig(
        **_tiny(memory=True, memory_config={"db_path": str(tmp_path / "mem.db")})
    )
    assert cfg.memory is True
    assert cfg.memory_config.db_path.endswith("mem.db")


def test_moe_top_k_must_not_exceed_experts() -> None:
    with pytest.raises(ConfigError, match="top_k"):
        MoEConfig(n_experts=2, top_k=3)


def test_moe_requires_at_least_two_experts() -> None:
    with pytest.raises(ConfigError, match="n_experts must be >= 2"):
        MoEConfig(n_experts=1)


def test_ssm_dt_range_validation() -> None:
    with pytest.raises(ConfigError, match="dt_min"):
        SSMConfig(dt_min=0.5, dt_max=0.1)
    with pytest.raises(ConfigError, match="dt_rank"):
        SSMConfig(dt_rank=0)


def test_trm_step_validation() -> None:
    with pytest.raises(ConfigError, match="min_steps"):
        TRMConfig(max_steps=2, min_steps=3)
    with pytest.raises(ConfigError, match="halt_threshold"):
        TRMConfig(halt_threshold=1.5)


def test_memory_config_rejects_blank_path() -> None:
    with pytest.raises(ConfigError, match="non-empty"):
        MemoryConfig(db_path="   ")


def test_sub_configs_round_trip() -> None:
    for cls in (MoEConfig, SSMConfig, TRMConfig, MemoryConfig):
        instance = cls.from_dict(cls().to_dict())
        assert instance == cls()


def test_unknown_sub_config_key_rejected() -> None:
    with pytest.raises(ConfigError, match="unknown MoEConfig key"):
        MoEConfig.from_dict({"n_experts": 2, "top_k": 1, "experts": 4})


# ---------------------------------------------------------------------------
# round trip to dict
# ---------------------------------------------------------------------------
def test_round_trip_to_dict() -> None:
    cfg = ModelConfig(
        **_tiny(
            gqa=True,
            n_kv_heads=2,
            moe=True,
            moe_config={"n_experts": 2, "top_k": 1},
            ssm=True,
            trm=True,
            verifier=True,
        )
    )
    restored = ModelConfig.from_dict(cfg.to_dict())
    assert restored == cfg
    assert restored.to_dict() == cfg.to_dict()


def test_to_dict_is_yaml_and_json_safe() -> None:
    import json

    data = ModelConfig(**_tiny()).to_dict()
    assert json.loads(json.dumps(data)) == data
    assert yaml.safe_load(yaml.safe_dump(data)) == data


def test_from_dict_rejects_non_mapping() -> None:
    with pytest.raises(ConfigError, match="expects a mapping"):
        ModelConfig.from_dict([1, 2, 3])  # type: ignore[arg-type]


def test_from_dict_rejects_bad_nested_type() -> None:
    with pytest.raises(ConfigError, match="moe_config must be a mapping"):
        ModelConfig.from_dict(_tiny(moe_config=5))
