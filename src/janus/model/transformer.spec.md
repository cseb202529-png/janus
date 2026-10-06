# Spec: `src/janus/model/transformer.py`
- **Label:** ESTABLISHED
- **Phase:** 04,11
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Stack of blocks according to layer pattern (e.g. A,S,A,S,A,S).

## Interface (inputs → outputs, with shapes where applicable)
ids→hidden [B,T,D].

## Required tests (CPU, tiny config)
Pattern parsing; depth; causality end-to-end.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
