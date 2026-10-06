# Spec: `src/janus/data/contamination.py`
- **Label:** ESTABLISHED
- **Phase:** 22
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Detect overlap with evaluation sets.

## Interface (inputs → outputs, with shapes where applicable)
train stream, eval sets→flagged docs report.

## Required tests (CPU, tiny config)
Planted overlap found.

## Notes / edge cases / risks
Mandatory before any release number.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
