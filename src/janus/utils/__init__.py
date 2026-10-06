"""Shared utilities: device detection, seeding, JSONL logging, reproducibility.

Modules (one per ``*.spec.md`` in this folder):

======================  =====  =========================================
Module                  Phase  Purpose
======================  =====  =========================================
``device``              01/02  Auto-detect CUDA/GPU/VRAM/BF16/FP16
``seed``                02     Global seeding incl. dataloader workers
``logging``             02     Structured JSONL logging
``reproducibility``     02     Config hash, git commit, env snapshot
``profiling``           08     Step timing / FLOPs utilisation
``metrics``             27     Training metric aggregation
======================  =====  =========================================

Deliberately no eager imports here: ``import janus.utils`` must not pull in
PyTorch. Import the submodule you need, e.g. ``from janus.utils.seed import set_seed``.
"""

from __future__ import annotations

__all__ = ["device", "seed", "logging", "reproducibility"]
