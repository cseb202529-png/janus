# Spec: `src/janus/inference/batching.py`
- **Label:** ESTABLISHED
- **Phase:** 47
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Batched generation with padding.

## Interface (inputs → outputs, with shapes where applicable)
-

## Required tests (CPU, tiny config)
Batch equals single results.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
