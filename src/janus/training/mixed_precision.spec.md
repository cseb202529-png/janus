# Spec: `src/janus/training/mixed_precision.py`
- **Label:** ESTABLISHED
- **Phase:** 27
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Auto-detect BF16/FP16/FP32 and scaling.

## Interface (inputs → outputs, with shapes where applicable)
-

## Required tests (CPU, tiny config)
CPU fallback; loss scale logic.

## Notes / edge cases / risks
Training component. Config-driven, resumable, logs JSONL.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
