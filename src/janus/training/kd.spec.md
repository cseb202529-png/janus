# Spec: `src/janus/training/kd.py`
- **Label:** ESTABLISHED
- **Phase:** 30
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Logit distillation (KL with temperature) from teacher outputs.

## Interface (inputs → outputs, with shapes where applicable)
student/teacher logits→loss.

## Required tests (CPU, tiny config)
Zero loss when identical; gradient only to student.

## Notes / edge cases / risks
Training component. Config-driven, resumable, logs JSONL.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
