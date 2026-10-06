#!/usr/bin/env python3
"""Report environment capabilities for Janus training/testing (Phase 01).

Reports: Python, pip, git, nvidia-smi, PyTorch, CUDA, GPU, VRAM, BF16/FP16 support,
and the device that `utils/device.py` would select.

No device is hard-coded: everything is detected at runtime. The script never fails
if an optional component (torch, git, nvidia-smi) is missing; it reports it as
missing instead.

Usage:
    python scripts/check_environment.py
"""

from __future__ import annotations

import importlib.util
import platform
import shutil
import subprocess
import sys


def _run_version(cmd: list[str]) -> str:
    """Return first line of `cmd --version` output, or 'not found'."""
    exe = shutil.which(cmd[0])
    if exe is None:
        return "not found"
    try:
        out = subprocess.run(
            [exe, *cmd[1:], "--version"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return f"error: {exc}"
    line = (out.stdout or out.stderr).strip().splitlines()
    return line[0] if line else "no output"


def _pip_version() -> str:
    try:
        from importlib.metadata import version

        return version("pip")
    except Exception as exc:  # pragma: no cover - pip always present in practice
        return f"unknown ({exc})"


def _report_torch() -> dict[str, str]:
    """Detect PyTorch + accelerator capabilities. Never raises."""
    info: dict[str, str] = {}
    if importlib.util.find_spec("torch") is None:
        info["torch"] = "not installed"
        info["device_selected"] = "cpu (torch missing)"
        return info

    import torch

    info["torch"] = torch.__version__
    info["cuda_available"] = str(torch.cuda.is_available())
    info["cuda_version"] = torch.version.cuda or "n/a"
    info["bf16_supported"] = str(
        torch.cuda.is_available() and torch.cuda.is_bf16_supported()
    )
    info["fp16_supported"] = str(torch.cuda.is_available())

    if torch.cuda.is_available():
        idx = torch.cuda.current_device()
        props = torch.cuda.get_device_properties(idx)
        vram_gib = props.total_memory / (1024**3)
        info["device_selected"] = f"cuda:{idx}"
        info["gpu"] = props.name
        info["vram_gib"] = f"{vram_gib:.2f}"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        info["device_selected"] = "mps"
        info["gpu"] = "Apple MPS"
    else:
        info["device_selected"] = "cpu"
        info["gpu"] = "none"
    return info


def main() -> int:
    print("== Janus environment check ==")
    print(f"python: {sys.version.split()[0]} ({sys.executable})")
    print(f"platform: {platform.platform()}")
    print(f"pip: {_pip_version()}")
    print(f"git: {_run_version(['git'])}")
    print(f"nvidia-smi: {_run_version(['nvidia-smi'])}")
    for key, value in _report_torch().items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
