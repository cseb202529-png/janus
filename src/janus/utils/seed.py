"""Global seeding, including PyTorch dataloader workers.

- **Label:** ESTABLISHED
- **Phase:** 02
- **Config flag:** none (``TrainingConfig.seed`` supplies the value).

Purpose
-------
Make runs reproducible: same seed → same numbers, on CPU and (when present) CUDA.

Interface
---------
``set_seed(seed, *, deterministic=False) -> dict``
    Seed ``random``, ``numpy.random``, ``torch`` (all CUDA devices if present).
    Output: ``dict`` describing what was seeded (JSON-serialisable).

``seed_worker(worker_id) -> None``
    ``worker_init_fn`` for ``torch.utils.data.DataLoader``: derives per-worker
    ``numpy``/``random`` seeds from ``torch.initial_seed()``.

``get_generator(seed, device="cpu") -> torch.Generator``
    Output: a seeded ``torch.Generator`` — pass as ``DataLoader(generator=...)``.

``isolated_seed(seed, deterministic=False)`` (context manager)
    Set the seed for a block, then restore every RNG state on exit. Used by tests
    so seeding does not leak between test cases.

Tensor shapes: **none** — no tensors are created or transformed; only RNG state
(``torch.ByteTensor`` for CPU state, list of ``ByteTensor`` for CUDA) is saved/restored.

Notes / edge cases / risks
--------------------------
* ``PYTHONHASHSEED`` is exported for *child* processes only; CPython ignores
  changes to it inside a running process. The returned dict states this honestly
  instead of claiming it took effect.
* ``numpy`` accepts seeds in ``[0, 2**32)``; larger seeds are folded modulo
  ``2**32`` (documented, deterministic).
* ``deterministic=True`` enables ``torch.use_deterministic_algorithms(True, warn_only=True)``
  so a missing deterministic kernel warns instead of crashing the run.
"""

from __future__ import annotations

import contextlib
import os
import random
from collections.abc import Iterator
from typing import Any

import numpy as np
import torch

_UINT32 = 2**32


def set_seed(seed: int, *, deterministic: bool = False) -> dict[str, Any]:
    """Seed every RNG Janus uses.

    Parameters
    ----------
    seed : int
        Non-negative integer (``TrainingConfig.seed``).
    deterministic : bool
        If ``True``, request deterministic algorithms (warn-only) and disable
        cuDNN autotuning. ``False`` restores the default, faster behaviour.

    Returns
    -------
    dict
        ``{"seed", "deterministic", "python", "numpy", "torch", "cuda",
        "cudnn_deterministic", "cudnn_benchmark", "pythonhashseed_scope"}``.
        All values are JSON-serialisable; **no tensors**.

    Raises
    ------
    ValueError
        ``seed`` is not an ``int`` (bools rejected) or is negative.
    """
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError(f"seed must be an int, got {type(seed).__name__}")
    if seed < 0:
        raise ValueError(f"seed must be a non-negative int, got {seed}")

    random.seed(seed)
    np.random.seed(seed % _UINT32)
    torch.manual_seed(seed)  # seeds CPU and all CUDA devices

    cuda_seeded = False
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        cuda_seeded = True

    os.environ["PYTHONHASHSEED"] = str(seed)

    torch.backends.cudnn.deterministic = deterministic
    torch.backends.cudnn.benchmark = not deterministic
    torch.use_deterministic_algorithms(deterministic, warn_only=True)

    return {
        "seed": seed,
        "deterministic": deterministic,
        "python": True,
        "numpy": True,
        "torch": True,
        "cuda": cuda_seeded,
        "cudnn_deterministic": deterministic,
        "cudnn_benchmark": not deterministic,
        "pythonhashseed_scope": "child processes only (CPython ignores runtime changes)",
    }


def seed_worker(worker_id: int) -> None:
    """``worker_init_fn`` for ``torch.utils.data.DataLoader``.

    Input: ``worker_id`` (int, provided by PyTorch). Derives a per-worker seed from
    ``torch.initial_seed()`` so each worker has an independent but reproducible
    ``numpy``/``random`` stream. Output: none (RNG state only, **no tensors**).
    """
    del worker_id  # torch.initial_seed() already encodes base_seed + worker_id
    worker_seed = torch.initial_seed() % _UINT32
    np.random.seed(worker_seed)
    random.seed(worker_seed)


def get_generator(seed: int, device: str = "cpu") -> torch.Generator:
    """Return a seeded ``torch.Generator`` for dataloaders/samplers.

    Parameters
    ----------
    seed : int
        Non-negative seed.
    device : str
        Generator device (``"cpu"`` default — the only value PyTorch fully
        supports for dataloaders).

    Returns
    -------
    torch.Generator
        Output: a generator whose state is ``seed``. **No tensor allocated here.**

    Raises
    ------
    ValueError
        ``seed`` is not a non-negative ``int``.
    """
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError(f"seed must be a non-negative int, got {seed!r}")
    generator = torch.Generator(device=device)
    generator.manual_seed(seed)
    return generator


@contextlib.contextmanager
def isolated_seed(seed: int, *, deterministic: bool = False) -> Iterator[dict[str, Any]]:
    """Seed inside the block, restore the previous RNG states on exit.

    Yields the same ``dict`` as :func:`set_seed`. Guarantees that callers
    (tests in particular) do not leak RNG state into later code.
    """
    py_state = random.getstate()
    np_state = np.random.get_state()
    torch_state = torch.get_rng_state()
    cuda_states = torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None
    cudnn_deterministic = torch.backends.cudnn.deterministic
    cudnn_benchmark = torch.backends.cudnn.benchmark

    try:
        yield set_seed(seed, deterministic=deterministic)
    finally:
        random.setstate(py_state)
        np.random.set_state(np_state)
        torch.set_rng_state(torch_state)
        if cuda_states is not None:
            torch.cuda.set_rng_state_all(cuda_states)
        torch.backends.cudnn.deterministic = cudnn_deterministic
        torch.backends.cudnn.benchmark = cudnn_benchmark


__all__ = ["set_seed", "seed_worker", "get_generator", "isolated_seed"]
