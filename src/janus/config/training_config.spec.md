# Spec: `src/janus/config/training_config.py`
- **Label:** ESTABLISHED
- **Phase:** 02
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Training hyperparameters config.

## Interface (inputs → outputs, with shapes where applicable)
YAML → TrainingConfig (optimizer, lr, warmup, schedule, clip, precision, accumulation, checkpoint interval, seed, eval interval).

## Required tests (CPU, tiny config)
Validation of ranges; round trip.

## Notes / edge cases / risks
No device or path hard-coding.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
