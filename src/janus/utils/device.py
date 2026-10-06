"""Device auto-detection: CUDA / GPU / VRAM / BF16 / FP16.

- **Label:** ESTABLISHED
- **Phase:** 01 (spec header) / delivered with Phase 02 (``phases/02_repository_bootstrap.md``
  lists ``utils/device`` as a deliverable).
- **Config flag:** none — this module is infrastructure, not an experimental component.

Purpose
-------
Report what the machine can actually do, and pick a ``torch.device`` / ``torch.dtype``
from a *caller-supplied preference*. Nothing is hard-coded: the default preference is
``"auto"``, and the caller normally forwards ``TrainingConfig.device`` and
``TrainingConfig.precision`` from YAML.

Interface
---------
``detect_device(preference: str = "auto") -> DeviceInfo``
    Returns a frozen record of the detected capabilities.
    Inputs: ``preference`` in ``{"auto", "cpu", "cuda", "mps"}``.
    Outputs: :class:`DeviceInfo` (strings/bools/floats — **no tensors**).

``get_device(preference: str = "auto") -> torch.device``
    Preference → ``torch.device``. Raises :class:`DeviceError` if an explicitly
    requested backend is unavailable; ``"auto"`` never raises (falls back
    cuda → mps → cpu).

``select_dtype(precision="auto", info=None) -> torch.dtype``
    Precision in ``{"auto", "fp32", "fp16", "bf16"}`` → dtype.
    ``"auto"`` prefers bf16, then fp16, else fp32.

``device_summary(info) -> dict``
    JSON-serialisable dict for logs/checkpoints.

Tensor shapes: **none** — this module never creates, moves or transforms tensors.

Notes / edge cases / risks
--------------------------
* BF16/FP16 support is reported *conservatively*: CPU reports both as unsupported so
  that ``precision: auto`` resolves to fp32 on CPU (half-precision CPU training is a
  common source of silent NaNs).
* MPS reports fp16 supported, bf16 unsupported.
* ``torch.cuda.is_bf16_supported()`` is only queried when CUDA is present, so
  CPU-only builds never touch it.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import torch

VALID_PREFERENCES: tuple[str, ...] = ("auto", "cpu", "cuda", "mps")
VALID_PRECISIONS: tuple[str, ...] = ("auto", "fp32", "fp16", "bf16")

_GIB = 1024**3


class DeviceError(RuntimeError):
    """Raised when a device/preference/dtype request cannot be satisfied."""


@dataclass(frozen=True)
class DeviceInfo:
    """Detected accelerator capabilities.

    Attributes
    ----------
    device : str
        Runnable device string, e.g. ``"cuda:0"``, ``"mps"``, ``"cpu"``.
    kind : str
        One of ``{"cuda", "mps", "cpu"}``.
    preference : str
        The preference that produced this record.
    cuda_available : bool
    cuda_version : str or None
        ``None`` when CUDA is unavailable or torch is a CPU build.
    gpu_name : str or None
        Human-readable accelerator name, ``None`` on CPU.
    vram_gib : float or None
        Total device memory in GiB, ``None`` on CPU.
    bf16_supported : bool
        Conservative: ``True`` only where mixed-precision bf16 is known-good.
    fp16_supported : bool
        Conservative: ``True`` only where mixed-precision fp16 is known-good.
    note : str
        Why the choice was made (surfaced in logs).
    """

    device: str
    kind: str
    preference: str
    cuda_available: bool
    cuda_version: str | None
    gpu_name: str | None
    vram_gib: float | None
    bf16_supported: bool
    fp16_supported: bool
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable dict. Output: ``dict[str, bool|float|str|None]``."""
        return asdict(self)


def _mps_available() -> bool:
    backends = getattr(torch.backends, "mps", None)
    if backends is None:
        return False
    try:
        return bool(backends.is_available())
    except Exception:  # pragma: no cover - defensive: backend probe must never crash
        return False


def detect_device(preference: str = "auto") -> DeviceInfo:
    """Detect accelerator capabilities for ``preference``.

    Parameters
    ----------
    preference : str
        ``"auto"`` (cuda → mps → cpu fallback), ``"cpu"``, ``"cuda"`` or ``"mps"``.

    Returns
    -------
    DeviceInfo
        Frozen capability record. **No tensors created.**

    Raises
    ------
    DeviceError
        Unknown preference, or an explicitly requested backend that is unavailable.
    """
    if not isinstance(preference, str) or preference not in VALID_PREFERENCES:
        raise DeviceError(
            f"unknown device preference {preference!r}; expected one of {VALID_PREFERENCES}"
        )

    cuda_ok = bool(torch.cuda.is_available())
    mps_ok = _mps_available()

    if preference == "cpu":
        kind, note = "cpu", "preference=cpu"
    elif preference == "cuda":
        if not cuda_ok:
            raise DeviceError(
                "preference='cuda' requested but torch.cuda.is_available() is False. "
                "Use device: auto (falls back to cpu) in the YAML config, or install a "
                "CUDA build of PyTorch."
            )
        kind, note = "cuda", "preference=cuda"
    elif preference == "mps":
        if not mps_ok:
            raise DeviceError(
                "preference='mps' requested but the MPS backend is unavailable. "
                "Use device: auto in the YAML config."
            )
        kind, note = "mps", "preference=mps"
    else:  # auto
        if cuda_ok:
            kind, note = "cuda", "auto: cuda available"
        elif mps_ok:
            kind, note = "mps", "auto: no cuda, mps available"
        else:
            kind, note = "cpu", "auto: no accelerator, cpu fallback"

    if kind == "cuda":
        idx = int(torch.cuda.current_device())
        props = torch.cuda.get_device_properties(idx)
        device = f"cuda:{idx}"
        gpu_name: str | None = str(props.name)
        vram_gib: float | None = float(props.total_memory) / _GIB
        cuda_version: str | None = str(torch.version.cuda) if torch.version.cuda else None
        try:
            bf16 = bool(torch.cuda.is_bf16_supported())
        except Exception:  # pragma: no cover - defensive
            bf16 = False
        fp16 = True
    elif kind == "mps":
        device, gpu_name, vram_gib, cuda_version = "mps", "Apple MPS", None, None
        bf16, fp16 = False, True
    else:
        device, gpu_name, vram_gib, cuda_version = "cpu", None, None, None
        # Conservative on purpose: half precision on CPU is a known NaN source.
        bf16, fp16 = False, False

    return DeviceInfo(
        device=device,
        kind=kind,
        preference=preference,
        cuda_available=cuda_ok,
        cuda_version=cuda_version,
        gpu_name=gpu_name,
        vram_gib=vram_gib,
        bf16_supported=bf16,
        fp16_supported=fp16,
        note=note,
    )


def get_device(preference: str = "auto") -> torch.device:
    """Preference → ``torch.device``.

    Output: ``torch.device`` — ``cuda:N`` / ``mps`` / ``cpu``. **No tensor allocated.**
    Raises :class:`DeviceError` for unknown or unavailable explicit preferences.
    """
    return torch.device(detect_device(preference).device)


def select_dtype(precision: str = "auto", info: DeviceInfo | None = None) -> torch.dtype:
    """Precision → ``torch.dtype``.

    Parameters
    ----------
    precision : str
        ``"auto"``, ``"fp32"``, ``"fp16"`` or ``"bf16"`` (from ``TrainingConfig.precision``).
    info : DeviceInfo, optional
        Reuse an existing detection instead of re-probing.

    Returns
    -------
    torch.dtype
        Output dtype for model weights/activations. **No tensor created.**

    Raises
    ------
    DeviceError
        Unknown precision, or an explicit half precision unsupported on this device.
    """
    if not isinstance(precision, str) or precision not in VALID_PRECISIONS:
        raise DeviceError(
            f"unknown precision {precision!r}; expected one of {VALID_PRECISIONS}"
        )
    info = info or detect_device()

    if precision == "fp32":
        return torch.float32
    if precision == "fp16":
        if not info.fp16_supported:
            raise DeviceError(
                f"precision='fp16' is not supported on device '{info.device}'. "
                "Set precision: auto or precision: fp32 in the YAML config."
            )
        return torch.float16
    if precision == "bf16":
        if not info.bf16_supported:
            raise DeviceError(
                f"precision='bf16' is not supported on device '{info.device}'. "
                "Set precision: auto or precision: fp32 in the YAML config."
            )
        return torch.bfloat16

    # auto
    if info.bf16_supported:
        return torch.bfloat16
    if info.fp16_supported:
        return torch.float16
    return torch.float32


def device_summary(info: DeviceInfo) -> dict[str, Any]:
    """JSON-serialisable summary for JSONL logs and checkpoint metadata.

    Input: :class:`DeviceInfo`. Output: ``dict[str, bool|float|str|None]`` with keys
    ``device, kind, cuda_available, cuda_version, gpu_name, vram_gib,
    bf16_supported, fp16_supported``.
    """
    data = info.to_dict()
    data.pop("preference", None)
    data.pop("note", None)
    return data


__all__ = [
    "VALID_PREFERENCES",
    "VALID_PRECISIONS",
    "DeviceError",
    "DeviceInfo",
    "detect_device",
    "get_device",
    "select_dtype",
    "device_summary",
]
