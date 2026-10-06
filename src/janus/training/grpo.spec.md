# Spec: `src/janus/training/grpo.py`
- **Label:** EXPERIMENTAL
- **Phase:** 38,39
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Group-relative policy optimization and gradient-balanced variant.

## Interface (inputs → outputs, with shapes where applicable)
prompts→groups→rewards→update.

## Required tests (CPU, tiny config)
Advantage normalization; clipping; compare standard vs balanced.

## Notes / edge cases / risks
Only after base, instruct, and eval exist.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
