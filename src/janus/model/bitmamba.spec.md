# Spec: `src/janus/model/bitmamba.py`
- **Label:** EXPERIMENTAL
- **Phase:** 10,46
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Low-bit experimental SSM variant.

## Interface (inputs → outputs, with shapes where applicable)
same as ssm.

## Required tests (CPU, tiny config)
Matches ssm in fp mode; quantized quality delta.

## Notes / edge cases / risks
Do last. Compare quality, size, speed, memory.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
