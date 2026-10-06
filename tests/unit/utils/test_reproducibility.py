"""Phase 02 tests for `janus/utils/reproducibility.py`.

Spec: config hash, git commit capture, environment snapshot. CPU only.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import pytest

from janus.config import ModelConfig, TrainingConfig
from janus.utils.reproducibility import (
    canonical_json,
    capture,
    config_hash,
    environment_snapshot,
    file_hash,
    git_snapshot,
)


def test_config_hash_is_stable_across_key_order() -> None:
    assert config_hash({"a": 1, "b": 2}) == config_hash({"b": 2, "a": 1})


def test_config_hash_changes_with_value() -> None:
    assert config_hash({"a": 1}) != config_hash({"a": 2})


def test_config_hash_is_sha256_hex() -> None:
    digest = config_hash({"x": 1})
    assert len(digest) == 64
    assert all(c in "0123456789abcdef" for c in digest)


def test_config_hash_of_dataclass_equals_its_dict() -> None:
    cfg = ModelConfig(vocab_size=256, d_model=32, n_heads=4, n_layers=2)
    assert config_hash(cfg) == config_hash(cfg.to_dict())


def test_config_hash_accepts_plain_string() -> None:
    assert config_hash("hello") == hashlib.sha256(
        canonical_json("hello").encode("utf-8")
    ).hexdigest()


def test_canonical_json_is_deterministic_and_compact() -> None:
    text = canonical_json({"b": [1, 2], "a": {"z": 1, "y": 2}})
    assert text == '{"a":{"y":2,"z":1},"b":[1,2]}'


def test_canonical_json_stringifies_non_finite() -> None:
    text = canonical_json({"v": float("nan")})
    assert "NaN" in text
    json.loads(text)  # strict JSON, always parseable


def test_file_hash_matches_hashlib(tmp_path: Path) -> None:
    path = tmp_path / "blob.bin"
    payload = b"janus" * 1000
    path.write_bytes(payload)
    assert file_hash(path) == hashlib.sha256(payload).hexdigest()


def test_file_hash_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        file_hash(tmp_path / "nope.bin")


def test_git_snapshot_shape() -> None:
    snap = git_snapshot()
    assert set(snap) == {"available", "commit", "branch", "dirty", "describe"}
    assert isinstance(snap["available"], bool)
    if snap["available"]:
        assert isinstance(snap["commit"], str)
        assert len(snap["commit"]) in (40, 64)  # sha1 or sha256 object format
        assert isinstance(snap["dirty"], bool)


def test_git_snapshot_never_raises_without_repo(tmp_path: Path) -> None:
    snap = git_snapshot(tmp_path)  # empty dir outside any work tree
    assert snap["available"] is False
    assert snap["commit"] is None


def test_environment_snapshot_keys_and_values() -> None:
    snap = environment_snapshot()
    expected = {
        "python_version",
        "python_implementation",
        "platform",
        "machine",
        "executable",
        "torch_version",
        "torch_cuda_version",
        "cuda_available",
        "gpu_count",
        "gpu_names",
    }
    assert set(snap) == expected
    assert snap["python_version"] == platform.python_version()
    assert snap["torch_version"] is not None
    assert isinstance(snap["cuda_available"], bool)
    assert json.loads(json.dumps(snap)) == snap


def test_capture_combines_all_parts() -> None:
    cfg = TrainingConfig(lr=1e-3, total_steps=10, warmup_steps=1)
    record = capture(cfg)
    assert record["config_hash"] == config_hash(cfg)
    assert record["config"]["lr"] == pytest.approx(1e-3)
    assert isinstance(record["git"], dict)
    assert isinstance(record["environment"], dict)
    assert json.loads(json.dumps(record)) == record


def test_capture_without_config() -> None:
    record = capture()
    assert record["config_hash"] is None
    assert record["config"] is None
    assert set(record) == {"config_hash", "config", "git", "environment"}


def test_capture_is_stable_for_identical_config() -> None:
    cfg = ModelConfig(vocab_size=512, d_model=64, n_heads=4, n_layers=2)
    assert capture(cfg)["config_hash"] == capture(cfg)["config_hash"]
