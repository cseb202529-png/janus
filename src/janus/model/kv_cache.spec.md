# Spec: `src/janus/model/kv_cache.py`
- **Label:** ESTABLISHED
- **Phase:** 26
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
KV cache structures for GQA, MLA latent, and SSM state.

## Interface (inputs → outputs, with shapes where applicable)
append/get/reset/crop.

## Required tests (CPU, tiny config)
Cached generation equals full recompute.

## Notes / edge cases / risks
Define interaction with TRM and routing.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
