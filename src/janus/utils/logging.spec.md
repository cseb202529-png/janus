# Spec: `src/janus/utils/logging.py`
- **Label:** ESTABLISHED
- **Phase:** 02
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Structured JSONL logging.

## Interface (inputs → outputs, with shapes where applicable)
-

## Required tests (CPU, tiny config)
Format and levels.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
