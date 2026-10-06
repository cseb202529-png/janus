# Spec: `src/janus/inference/kv_cache.py`
- **Label:** ESTABLISHED
- **Phase:** 47
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Inference-side cache manager (wraps model/kv_cache).

## Interface (inputs → outputs, with shapes where applicable)
-

## Required tests (CPU, tiny config)
Memory growth bounds.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
