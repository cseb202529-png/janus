"""Phase 02: package skeleton, version, and import surface."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_import_janus() -> None:
    """Gate: `import janus` works."""
    import janus

    assert isinstance(janus.__version__, str) and janus.__version__


def test_version_matches_pyproject() -> None:
    """Single source of truth: pyproject `project.version` == `janus.__version__`."""
    import janus

    pyproject = REPO_ROOT / "pyproject.toml"
    with pyproject.open("rb") as handle:
        data = tomllib.load(handle)
    assert data["project"]["version"] == janus.__version__


def test_config_package_exports() -> None:
    """`from janus.config import ...` exposes the Phase 02 configs."""
    import janus.config as cfg

    for name in (
        "ModelConfig",
        "TrainingConfig",
        "DataConfig",
        "MoEConfig",
        "SSMConfig",
        "TRMConfig",
        "MemoryConfig",
        "ConfigError",
    ):
        assert hasattr(cfg, name), f"janus.config does not export {name}"
        assert name in cfg.__all__


@pytest.mark.parametrize(
    "subpackage",
    [
        "adapters",
        "api",
        "cli",
        "data",
        "distillation",
        "evaluation",
        "inference",
        "memory",
        "model",
        "tokenizer",
        "training",
        "ui",
        "utils",
        "config",
    ],
)
def test_package_skeleton_importable(subpackage: str) -> None:
    """Every package in the skeleton has an `__init__.py` and imports cleanly."""
    module = __import__(f"janus.{subpackage}", fromlist=["__all__"])
    assert module is not None


def test_utils_package_does_not_eagerly_import_torch() -> None:
    """`import janus.utils` must stay cheap (no eager torch import)."""
    import subprocess
    import sys

    code = (
        "import sys, janus.utils;"
        "raise SystemExit(0 if 'torch' not in sys.modules else 1)"
    )
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert proc.returncode == 0, f"janus.utils pulled in torch: {proc.stderr}"
