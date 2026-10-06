"""Phase 02 tests for `janus/config/data_config.py`.

Required by `src/janus/config/data_config.spec.md`:
validation; round trip. CPU only, tiny configs.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import janus.config.data_config as data_module
from janus.config import ConfigError, DataConfig


def test_defaults_documented_in_docstring() -> None:
    module_doc = data_module.__doc__ or ""
    for token in ("``packing_length``", "``512``", "``dedup_algorithm``", "minhash"):
        assert token in module_doc, f"defaults table is missing {token!r}"


def test_documented_default_values() -> None:
    cfg = DataConfig()
    assert cfg.sources == []
    assert cfg.tokenizer_ref is None  # nothing hard-coded
    assert cfg.min_doc_len == 1
    assert cfg.max_doc_len == 100_000
    assert cfg.language_filter == ["en"]
    assert cfg.min_quality_score == pytest.approx(0.0)
    assert cfg.safety_filter is True
    assert cfg.contamination_filter is True
    assert cfg.dedup is True
    assert cfg.dedup_algorithm == "minhash"
    assert cfg.dedup_threshold == pytest.approx(0.8)
    assert cfg.shard_size == 100_000
    assert cfg.packing_length == 512
    assert cfg.max_tokens is None
    assert cfg.cache_dir is None  # no path hard-coded
    assert cfg.drop_remainder is True


# ---------------------------------------------------------------------------
# round trip
# ---------------------------------------------------------------------------
def test_round_trip_to_dict() -> None:
    cfg = DataConfig(
        sources=["datasets/v1.jsonl"],
        tokenizer_ref="checkpoints/tok",
        packing_length=128,
        dedup_threshold=0.9,
    )
    assert DataConfig.from_dict(cfg.to_dict()) == cfg
    assert DataConfig.from_dict(cfg.to_dict()).to_dict() == cfg.to_dict()


def test_yaml_round_trip(tmp_path: Path) -> None:
    original = DataConfig(
        sources=["a.jsonl", "b.jsonl"],
        language_filter=["en", "de"],
        max_tokens=1000,
        dedup=False,
    )
    path = tmp_path / "data.yaml"
    path.write_text(yaml.safe_dump(original.to_dict()), encoding="utf-8")
    assert DataConfig.from_yaml(path) == original


def test_from_yaml_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not found"):
        DataConfig.from_yaml(tmp_path / "nope.yaml")


def test_from_yaml_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")
    with pytest.raises(ConfigError, match="empty"):
        DataConfig.from_yaml(path)


def test_to_dict_is_yaml_and_json_safe() -> None:
    import json

    data = DataConfig().to_dict()
    assert json.loads(json.dumps(data)) == data
    assert yaml.safe_load(yaml.safe_dump(data)) == data


def test_unknown_key_rejected() -> None:
    with pytest.raises(ConfigError, match="unknown DataConfig key"):
        DataConfig.from_dict({"batch_size": 4})


def test_from_dict_rejects_non_mapping() -> None:
    with pytest.raises(ConfigError, match="expects a mapping"):
        DataConfig.from_dict([])  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------
def test_reject_min_doc_len_above_max() -> None:
    with pytest.raises(ConfigError, match="max_doc_len .* must be >= min_doc_len"):
        DataConfig(min_doc_len=100, max_doc_len=10)


def test_reject_non_positive_doc_limits() -> None:
    with pytest.raises(ConfigError, match="min_doc_len must be >= 1"):
        DataConfig(min_doc_len=0)
    with pytest.raises(ConfigError, match="max_doc_len must be >= 1"):
        DataConfig(max_doc_len=0)


def test_reject_bad_quality_score() -> None:
    with pytest.raises(ConfigError, match="min_quality_score must be in"):
        DataConfig(min_quality_score=1.5)
    with pytest.raises(ConfigError, match="min_quality_score must be in"):
        DataConfig(min_quality_score=-0.1)


def test_reject_bad_dedup_threshold() -> None:
    with pytest.raises(ConfigError, match="dedup_threshold must be in"):
        DataConfig(dedup_threshold=1.2)


def test_reject_unknown_dedup_algorithm() -> None:
    with pytest.raises(ConfigError, match="dedup_algorithm must be one of"):
        DataConfig(dedup_algorithm="lsh-ish")


def test_reject_non_string_source() -> None:
    with pytest.raises(ConfigError, match=r"sources\[1\] must be a non-empty str"):
        DataConfig(sources=["ok", 42])


def test_reject_non_list_sources() -> None:
    with pytest.raises(ConfigError, match="sources must be a list"):
        DataConfig(sources="one.jsonl")  # type: ignore[arg-type]


def test_reject_blank_language_tag() -> None:
    with pytest.raises(ConfigError, match=r"language_filter\[0\] must be a non-empty str"):
        DataConfig(language_filter=[""])


def test_reject_non_positive_shard_and_packing() -> None:
    with pytest.raises(ConfigError, match="shard_size must be >= 1"):
        DataConfig(shard_size=0)
    with pytest.raises(ConfigError, match="packing_length must be >= 1"):
        DataConfig(packing_length=0)


def test_reject_bad_optional_caps() -> None:
    with pytest.raises(ConfigError, match="max_tokens must be >= 1"):
        DataConfig(max_tokens=0)
    with pytest.raises(ConfigError, match="max_documents must be >= 1"):
        DataConfig(max_documents=0)


def test_reject_blank_cache_dir() -> None:
    with pytest.raises(ConfigError, match="cache_dir"):
        DataConfig(cache_dir="")


def test_reject_bool_where_int_expected() -> None:
    with pytest.raises(ConfigError, match="shard_size must be an int"):
        DataConfig.from_dict({"shard_size": True})


def test_reject_non_bool_drop_remainder() -> None:
    with pytest.raises(ConfigError, match="drop_remainder must be a bool"):
        DataConfig(drop_remainder=1)


def test_empty_language_filter_is_allowed() -> None:
    """An empty language filter means 'no language filtering'."""
    cfg = DataConfig(language_filter=[])
    assert cfg.language_filter == []


def test_optional_caps_accept_none() -> None:
    cfg = DataConfig(max_tokens=None, max_documents=None, cache_dir=None)
    assert cfg.max_tokens is None
    assert cfg.max_documents is None
    assert cfg.cache_dir is None
