# Spec: `src/janus/training/bread.py`
- **Label:** EXPERIMENTAL
- **Phase:** 40
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Expert anchors, branched rollouts, ranking, branch selection.

## Interface (inputs → outputs, with shapes where applicable)
-

## Required tests (CPU, tiny config)
Mock rollouts.

## Notes / edge cases / risks
Experimental, not a pretraining dependency.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
