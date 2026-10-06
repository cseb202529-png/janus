# Spec: `src/janus/model/thought_engine.py`
- **Label:** EXPERIMENTAL
- **Phase:** 15
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Hidden iterative refinement module over latent state; no exposed chain-of-thought required.

## Interface (inputs → outputs, with shapes where applicable)
[B,T,D]→[B,T,D] with k refinement steps.

## Required tests (CPU, tiny config)
Steps configurable; k=0 equals identity path; gradients; compute cost reported.

## Notes / edge cases / risks
Optimizes reasoning performance via hidden states.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
