# Spec: `src/janus/training/checkpoint.py`
- **Label:** ESTABLISHED
- **Phase:** 29
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Save/load model, optimizer, scheduler, tokenizer, config, RNG, metrics.

## Interface (inputs → outputs, with shapes where applicable)
-

## Required tests (CPU, tiny config)
Save/load/resume identical; version tags.

## Notes / edge cases / risks
Training component. Config-driven, resumable, logs JSONL.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
