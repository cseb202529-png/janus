# Spec: `src/janus/cli/evaluate.py`
- **Label:** ESTABLISHED
- **Phase:** 51
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
CLI: run evals on a checkpoint.

## Interface (inputs → outputs, with shapes where applicable)
--checkpoint --suite

## Required tests (CPU, tiny config)
Smoke run.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
