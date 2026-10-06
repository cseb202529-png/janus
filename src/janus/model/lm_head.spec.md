# Spec: `src/janus/model/lm_head.py`
- **Label:** ESTABLISHED
- **Phase:** 04
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Output projection tied to embeddings.

## Interface (inputs → outputs, with shapes where applicable)
[B,T,D]→[B,T,V].

## Required tests (CPU, tiny config)
Tying; logits shape.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
