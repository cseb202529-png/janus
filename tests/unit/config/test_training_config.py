"""Phase 02 tests for `janus/config/training_config.py`.

Required by `src/janus/config/training_config.spec.md`:
validation of ranges; round trip. CPU only, tiny configs.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import janus.config.training_config as training_module
from janus.config import ConfigError, TrainingConfig


def test_defaults_documented_in_docstring() -> None:
    module_doc = training_module.__doc__ or ""
    for token in ("``lr``", "``3.0e-4``", "``seed``", "``1337``", "``batch_size``"):
        assert token in module_doc, f"defaults table is missing {token!r}"


def test_documented_default_values() -> None:
    cfg = TrainingConfig()
    assert cfg.optimizer == "adamw"
    assert cfg.lr == pytest.approx(3.0e-4)
    assert cfg.min_lr == pytest.approx(1.0e-5)
    assert cfg.weight_decay == pytest.approx(0.1)
    assert cfg.beta1 == pytest.approx(0.9)
    assert cfg.beta2 == pytest.approx(0.95)
    assert cfg.warmup_steps == 1000
    assert cfg.total_steps == 100_000
    assert cfg.schedule == "cosine"
    assert cfg.grad_clip == pytest.approx(1.0)
    assert cfg.precision == "auto"
    assert cfg.grad_accum_steps == 1
    assert cfg.batch_size == 8
    assert cfg.seed == 1337
    assert cfg.device == "auto"
    assert cfg.num_workers == 0
    assert cfg.resume_from is None
    assert cfg.deterministic is False


def test_no_device_or_path_hardcoded() -> None:
    """Device/precision come from config, never from source."""
    cfg = TrainingConfig()
    assert cfg.device == "auto"
    assert cfg.precision == "auto"
    assert cfg.resume_from is None


# ---------------------------------------------------------------------------
# round trip
# ---------------------------------------------------------------------------
def test_round_trip_to_dict() -> None:
    cfg = TrainingConfig(lr=1e-3, warmup_steps=10, total_steps=100, seed=7)
    assert TrainingConfig.from_dict(cfg.to_dict()) == cfg
    assert TrainingConfig.from_dict(cfg.to_dict()).to_dict() == cfg.to_dict()


def test_yaml_round_trip(tmp_path: Path) -> None:
    original = TrainingConfig(lr=5e-4, batch_size=2, precision="fp32", device="cpu")
    path = tmp_path / "training.yaml"
    path.write_text(yaml.safe_dump(original.to_dict()), encoding="utf-8")
    assert TrainingConfig.from_yaml(path) == original


def test_from_yaml_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not found"):
        TrainingConfig.from_yaml(tmp_path / "nope.yaml")


def test_from_yaml_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")
    with pytest.raises(ConfigError, match="empty"):
        TrainingConfig.from_yaml(path)


def test_to_dict_is_yaml_and_json_safe() -> None:
    import json

    data = TrainingConfig().to_dict()
    assert json.loads(json.dumps(data)) == data
    assert yaml.safe_load(yaml.safe_dump(data)) == data


def test_unknown_key_rejected() -> None:
    with pytest.raises(ConfigError, match="unknown TrainingConfig key"):
        TrainingConfig.from_dict({"learning_rate": 1e-3})


def test_from_dict_rejects_non_mapping() -> None:
    with pytest.raises(ConfigError, match="expects a mapping"):
        TrainingConfig.from_dict("lr: 0.1")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# range validation
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("bad_lr", [0.0, -1.0, 2.0, float("nan"), float("inf")])
def test_reject_bad_lr(bad_lr: float) -> None:
    with pytest.raises(ConfigError, match="lr must be"):
        TrainingConfig.from_dict({"lr": bad_lr})


def test_reject_min_lr_above_lr() -> None:
    with pytest.raises(ConfigError, match="min_lr .* must be <= lr"):
        TrainingConfig(lr=1e-4, min_lr=1e-3)


def test_reject_total_steps_not_greater_than_warmup() -> None:
    with pytest.raises(ConfigError, match="total_steps .* must be > warmup_steps"):
        TrainingConfig(warmup_steps=100, total_steps=100)


def test_reject_negative_warmup() -> None:
    with pytest.raises(ConfigError, match="warmup_steps must be >= 0"):
        TrainingConfig(warmup_steps=-1)


@pytest.mark.parametrize(
    "field,value",
    [
        ("weight_decay", -0.1),
        ("weight_decay", 1.5),
        ("beta1", 1.0),
        ("beta2", -0.1),
        ("eps", 0.0),
        ("grad_clip", -1.0),
        ("grad_accum_steps", 0),
        ("batch_size", 0),
        ("eval_interval", 0),
        ("log_interval", 0),
        ("checkpoint_interval", 0),
        ("keep_last_checkpoints", 0),
        ("seed", -1),
        ("num_workers", -1),
    ],
)
def test_reject_out_of_range_fields(field: str, value: float | int) -> None:
    with pytest.raises(ConfigError, match=field.replace("_", r"_")):
        TrainingConfig.from_dict({field: value})


@pytest.mark.parametrize(
    "field,value",
    [("optimizer", "sgd2"), ("schedule", "step"), ("precision", "fp8"), ("device", "tpu")],
)
def test_reject_unknown_choice(field: str, value: str) -> None:
    with pytest.raises(ConfigError, match="must be one of"):
        TrainingConfig.from_dict({field: value})


def test_reject_bool_where_int_expected() -> None:
    with pytest.raises(ConfigError, match="batch_size must be an int"):
        TrainingConfig.from_dict({"batch_size": True})


def test_reject_non_string_choice() -> None:
    with pytest.raises(ConfigError, match="optimizer must be one of"):
        TrainingConfig.from_dict({"optimizer": 1})


def test_reject_blank_resume_from() -> None:
    with pytest.raises(ConfigError, match="resume_from"):
        TrainingConfig(resume_from="   ")


def test_reject_non_bool_deterministic() -> None:
    with pytest.raises(ConfigError, match="deterministic must be a bool"):
        TrainingConfig(deterministic=1)


def test_resume_from_accepts_path(tmp_path: Path) -> None:
    cfg = TrainingConfig(resume_from=str(tmp_path / "ckpt.pt"))
    assert cfg.resume_from is not None
