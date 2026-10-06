# Spec: `src/janus/training/model_merging.py`
- **Label:** EXPERIMENTAL
- **Phase:** 41,45
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Adapter and weight merging, soup of experts.

## Interface (inputs → outputs, with shapes where applicable)
checkpoints→merged.

## Required tests (CPU, tiny config)
Merge of identical checkpoints is identity.

## Notes / edge cases / risks
Evaluate every merge.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
