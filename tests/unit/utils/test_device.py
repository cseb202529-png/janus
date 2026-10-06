"""Phase 02 tests for `janus/utils/device.py`.

Spec: CPU fallback; never hard-code CUDA. Every assertion is written so it holds
on a CPU-only box *and* on a GPU box — nothing assumes a particular machine.
"""

from __future__ import annotations

import dataclasses
import json

import pytest
import torch

from janus.utils.device import (
    VALID_PRECISIONS,
    VALID_PREFERENCES,
    DeviceError,
    DeviceInfo,
    detect_device,
    device_summary,
    get_device,
    select_dtype,
)


def test_cpu_fallback_explicit() -> None:
    """Required test: CPU fallback."""
    info = detect_device("cpu")
    assert info.kind == "cpu"
    assert info.device == "cpu"
    assert info.preference == "cpu"
    assert info.gpu_name is None
    assert info.vram_gib is None
    assert info.cuda_version is None
    # Conservative reporting: half precision is not claimed on CPU.
    assert info.bf16_supported is False
    assert info.fp16_supported is False
    assert isinstance(info.note, str) and info.note


def test_auto_never_raises() -> None:
    info = detect_device("auto")
    assert info.kind in ("cuda", "mps", "cpu")
    assert info.device == "cpu" or info.device.startswith(info.kind)
    if info.kind == "cpu":
        assert info.device == "cpu"
    elif info.kind == "cuda":
        assert info.device.startswith("cuda:")


def test_unknown_preference_rejected() -> None:
    with pytest.raises(DeviceError, match="unknown device preference"):
        detect_device("tpu")
    with pytest.raises(DeviceError, match="unknown device preference"):
        detect_device("")  # type: ignore[arg-type]
    with pytest.raises(DeviceError, match="unknown device preference"):
        detect_device(True)  # type: ignore[arg-type]


def test_explicit_cuda_requires_hardware() -> None:
    """Never hard-code CUDA: requesting it must fail loudly if absent."""
    if detect_device("auto").cuda_available:
        assert detect_device("cuda").kind == "cuda"
    else:
        with pytest.raises(DeviceError, match="cuda"):
            detect_device("cuda")


def test_explicit_mps_requires_hardware() -> None:
    auto = detect_device("auto")
    mps_backend = getattr(torch.backends, "mps", None)
    mps_available = bool(mps_backend is not None and mps_backend.is_available())
    if mps_available:
        assert detect_device("mps").kind == "mps"
    else:
        with pytest.raises(DeviceError, match="mps"):
            detect_device("mps")


def test_get_device_returns_torch_device() -> None:
    device = get_device("cpu")
    assert isinstance(device, torch.device)
    assert device.type == "cpu"


def test_get_device_matches_detection() -> None:
    info = detect_device("auto")
    assert get_device("auto") == torch.device(info.device)


def test_select_dtype_fp32_always_allowed() -> None:
    assert select_dtype("fp32", detect_device("cpu")) is torch.float32


def test_select_dtype_auto_matches_reported_capabilities() -> None:
    info = detect_device("auto")
    dtype = select_dtype("auto", info)
    assert dtype in (torch.float32, torch.float16, torch.bfloat16)
    if info.kind == "cpu":
        assert dtype is torch.float32
    elif info.bf16_supported:
        assert dtype is torch.bfloat16
    elif info.fp16_supported:
        assert dtype is torch.float16


def test_select_dtype_rejects_unsupported_precision() -> None:
    info = detect_device("cpu")
    if not info.bf16_supported:
        with pytest.raises(DeviceError, match="bf16"):
            select_dtype("bf16", info)
    if not info.fp16_supported:
        with pytest.raises(DeviceError, match="fp16"):
            select_dtype("fp16", info)


def test_select_dtype_unknown_precision() -> None:
    with pytest.raises(DeviceError, match="unknown precision"):
        select_dtype("fp8", detect_device("cpu"))


def test_valid_lists() -> None:
    assert VALID_PREFERENCES == ("auto", "cpu", "cuda", "mps")
    assert VALID_PRECISIONS == ("auto", "fp32", "fp16", "bf16")


def test_device_info_is_frozen() -> None:
    info = detect_device("cpu")
    with pytest.raises(dataclasses.FrozenInstanceError):
        info.device = "cuda:0"  # type: ignore[misc]


def test_device_info_to_dict_is_json_safe() -> None:
    info = detect_device("auto")
    data = info.to_dict()
    assert json.loads(json.dumps(data)) == data
    assert data["kind"] == info.kind


def test_device_summary_keys() -> None:
    summary = device_summary(detect_device("auto"))
    expected = {
        "device",
        "kind",
        "cuda_available",
        "cuda_version",
        "gpu_name",
        "vram_gib",
        "bf16_supported",
        "fp16_supported",
    }
    assert set(summary) == expected
    assert "preference" not in summary
    assert json.loads(json.dumps(summary)) == summary


def test_report_contains_no_nan_or_inf() -> None:
    info = detect_device("auto")
    for key, value in info.to_dict().items():
        text = str(value).lower()
        assert "nan" not in text, f"{key} reported {value!r}"
        assert text not in ("inf", "-inf", "infinity"), f"{key} reported {value!r}"
