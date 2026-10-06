# Spec: `src/janus/model/verifier.py`
- **Label:** EXPERIMENTAL
- **Phase:** 18
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Lightweight verification head/module for arithmetic, logic, consistency, structured output.

## Interface (inputs → outputs, with shapes where applicable)
hidden→accept score / continue signal.

## Required tests (CPU, tiny config)
Planted correct/incorrect examples; connects to TRM.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
