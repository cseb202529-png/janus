# Spec: `src/janus/model/hybrid_block.py`
- **Label:** ESTABLISHED
- **Phase:** 11
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Block combining mixer (attention or SSM) + FFN/MoE with RMSNorm and residuals.

## Interface (inputs → outputs, with shapes where applicable)
[B,T,D]→[B,T,D].

## Required tests (CPU, tiny config)
Each mixer type; residual path; layer pattern from config.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
