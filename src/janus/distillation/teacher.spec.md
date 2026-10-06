# Spec: `src/janus/distillation/teacher.py`
- **Label:** EXPERIMENTAL
- **Phase:** 30
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Teacher interface abstraction (API or local) with identity logging.

## Interface (inputs → outputs, with shapes where applicable)
prompt→response (+logits if available).

## Required tests (CPU, tiny config)
Mock teacher.

## Notes / edge cases / risks
Record teacher identity and terms.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
