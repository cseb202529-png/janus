"""Phase 02 tests for `janus/utils/seed.py`.

Spec required test: same seed → same result. CPU only, tiny tensors.
"""

from __future__ import annotations

import random

import numpy as np
import pytest
import torch

from janus.utils.seed import get_generator, isolated_seed, seed_worker, set_seed


def test_same_seed_same_torch_result() -> None:
    set_seed(123)
    first = torch.randn(8)
    set_seed(123)
    second = torch.randn(8)
    assert torch.equal(first, second)


def test_same_seed_same_numpy_result() -> None:
    set_seed(7)
    first = np.random.rand(8)
    set_seed(7)
    second = np.random.rand(8)
    assert np.array_equal(first, second)


def test_same_seed_same_python_result() -> None:
    set_seed(7)
    first = [random.random() for _ in range(8)]
    set_seed(7)
    second = [random.random() for _ in range(8)]
    assert first == second


def test_different_seed_different_result() -> None:
    set_seed(1)
    first = torch.randn(64)
    set_seed(2)
    second = torch.randn(64)
    assert not torch.equal(first, second)


def test_set_seed_returns_report() -> None:
    report = set_seed(42, deterministic=True)
    assert report["seed"] == 42
    assert report["deterministic"] is True
    assert report["python"] is True
    assert report["numpy"] is True
    assert report["torch"] is True
    assert isinstance(report["cuda"], bool)
    assert report["cudnn_deterministic"] is True
    assert "pythonhashseed_scope" in report
    # report must be JSON-serialisable for the JSONL logger
    import json

    assert json.loads(json.dumps(report)) == report


def test_set_seed_rejects_invalid_seed() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        set_seed(-1)
    with pytest.raises(ValueError, match="int"):
        set_seed(True)
    with pytest.raises(ValueError, match="int"):
        set_seed(1.5)  # type: ignore[arg-type]


def test_set_seed_toggles_deterministic_flag() -> None:
    set_seed(0, deterministic=True)
    assert torch.backends.cudnn.deterministic is True
    set_seed(0, deterministic=False)
    assert torch.backends.cudnn.deterministic is False


def test_get_generator_reproducible() -> None:
    gen_a = get_generator(99)
    gen_b = get_generator(99)
    assert torch.equal(torch.randn(4, generator=gen_a), torch.randn(4, generator=gen_b))


def test_get_generator_rejects_invalid_seed() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        get_generator(-5)


def test_seed_worker_is_deterministic() -> None:
    """DataLoader worker seeding: same torch seed → same numpy stream."""
    torch.manual_seed(11)
    seed_worker(0)
    first = np.random.rand(4)
    torch.manual_seed(11)
    seed_worker(0)
    second = np.random.rand(4)
    assert np.array_equal(first, second)


def test_seed_worker_differs_per_base_seed() -> None:
    torch.manual_seed(1)
    seed_worker(0)
    first = np.random.rand(4)
    torch.manual_seed(2)
    seed_worker(0)
    second = np.random.rand(4)
    assert not np.array_equal(first, second)


def test_isolated_seed_restores_state() -> None:
    set_seed(0)
    before = torch.randn(4)
    python_before = random.random()

    set_seed(0)
    with isolated_seed(777) as report:
        assert report["seed"] == 777
        inside = torch.randn(4)
        inside_python = random.random()

    after = torch.randn(4)
    python_after = random.random()

    # state fully restored → stream continues exactly where it left off
    assert torch.equal(before, after)
    assert python_before == python_after
    # the isolated block really used a different seed
    assert not torch.equal(before, inside)
    assert python_before != inside_python


def test_isolated_seed_restores_on_exception() -> None:
    set_seed(5)
    expected = torch.randn(4)

    set_seed(5)
    with pytest.raises(RuntimeError, match="boom"):
        with isolated_seed(1234):
            torch.randn(4)
            raise RuntimeError("boom")

    assert torch.equal(torch.randn(4), expected)


def test_isolated_seed_nested() -> None:
    set_seed(3)
    with isolated_seed(3):
        outer_first = torch.randn(4)
        with isolated_seed(9):
            inner = torch.randn(4)
        outer_second = torch.randn(4)

    set_seed(3)
    assert torch.equal(torch.randn(4), outer_first)
    # inner block used its own seed and did not perturb the outer stream
    assert not torch.equal(outer_first, inner)
    set_seed(3)
    _ = torch.randn(4)
    assert torch.equal(torch.randn(4), outer_second)
