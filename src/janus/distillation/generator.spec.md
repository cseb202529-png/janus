# Spec: `src/janus/distillation/generator.py`
- **Label:** EXPERIMENTAL
- **Phase:** 31,32
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Generate instruction data across categories.

## Interface (inputs → outputs, with shapes where applicable)
prompts→candidates.

## Required tests (CPU, tiny config)
Category coverage.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
