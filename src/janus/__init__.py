"""Janus: research-grade ~125M decoder-only autoregressive language model.

Labels: every component is marked ESTABLISHED or EXPERIMENTAL in its module
docstring and in ``docs/specification.md``.

Importing this package must stay cheap: it only exposes metadata. Subpackages
are imported explicitly, e.g. ``from janus.config import ModelConfig``.

Attributes
----------
__version__ : str
    Single Python-side version string. It must match ``project.version`` in
    ``pyproject.toml`` (enforced by ``tests/unit/test_package.py``).
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
