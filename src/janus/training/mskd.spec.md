# Spec: `src/janus/training/mskd.py`
- **Label:** EXPERIMENTAL
- **Phase:** 34
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Multi-step KD: output, hidden-state, intermediate (optional attention) distillation with projection layers when dims differ.

## Interface (inputs → outputs, with shapes where applicable)
-

## Required tests (CPU, tiny config)
Loss terms toggle; dims adapter shapes.

## Notes / edge cases / risks
Training component. Config-driven, resumable, logs JSONL.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
