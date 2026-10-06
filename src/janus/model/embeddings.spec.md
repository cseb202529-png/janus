# Spec: `src/janus/model/embeddings.py`
- **Label:** ESTABLISHED
- **Phase:** 04
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Token embedding with tie support.

## Interface (inputs → outputs, with shapes where applicable)
ids [B,T] → [B,T,D].

## Required tests (CPU, tiny config)
Shape; tying shares storage with lm_head.

## Notes / edge cases / risks
Model component. Document every tensor shape; support the config flag; expose param count.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
