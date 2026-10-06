# Spec: `src/janus/training/fdd.py`
- **Label:** EXPERIMENTAL
- **Phase:** 33
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Feedback-driven distillation loop.

## Interface (inputs → outputs, with shapes where applicable)
student outputs→reviewer feedback→training signal.

## Required tests (CPU, tiny config)
Loop runs on mock teacher.

## Notes / edge cases / risks
Training component. Config-driven, resumable, logs JSONL.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
