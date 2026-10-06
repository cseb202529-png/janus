# Spec: `src/janus/training/trainer.py`
- **Label:** ESTABLISHED
- **Phase:** 07,27
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Main training loop.

## Interface (inputs → outputs, with shapes where applicable)
configs+model+dataloader→checkpoints+metrics.

## Required tests (CPU, tiny config)
Tiny run loss decreases; resume reproduces; grad accumulation equals big batch.

## Notes / edge cases / risks
Training component. Config-driven, resumable, logs JSONL.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
