"""Phase 01 tests for `scripts/check_environment.py`.

Runs on CPU with no GPU required. The script must never raise when an optional
component (torch, git, nvidia-smi) is missing; it must report it instead.

Shapes: n/a — this module reports strings only, no tensors.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / "scripts" / "check_environment.py"

# Keys the environment report must always contain, present or not.
REQUIRED_KEYS = (
    "torch",
    "device_selected",
)


def _load_script_module():
    """Import scripts/check_environment.py as a module without executing main()."""
    spec = importlib.util.spec_from_file_location("check_environment", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_script_exists() -> None:
    assert SCRIPT.is_file(), f"missing Phase 01 deliverable: {SCRIPT}"


def test_main_returns_zero() -> None:
    mod = _load_script_module()
    assert mod.main() == 0


def test_report_torch_never_raises_and_is_complete() -> None:
    """CPU fallback: works with or without torch installed, never raises."""
    mod = _load_script_module()
    info = mod._report_torch()
    assert isinstance(info, dict)
    for key in REQUIRED_KEYS:
        assert key in info, f"missing report key: {key}"
    # No NaN/Inf can appear: values must be plain printable strings.
    for key, value in info.items():
        assert isinstance(key, str) and isinstance(value, str)
        assert "nan" not in value.lower() and "inf" not in value.lower()


def test_version_helpers_never_raise() -> None:
    mod = _load_script_module()
    assert isinstance(mod._run_version(["git"]), str)
    assert isinstance(mod._run_version(["definitely_not_a_real_binary_xyz"]), str)
    assert isinstance(mod._pip_version(), str)


def test_subprocess_entrypoint_prints_report() -> None:
    """End-to-end: `python scripts/check_environment.py` exits 0 and reports."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(REPO_ROOT),
    )
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout
    assert "Janus environment check" in out
    for key in REQUIRED_KEYS:
        assert f"{key}:" in out, f"report line missing from stdout: {key}"
    assert "nan" not in out.lower()
