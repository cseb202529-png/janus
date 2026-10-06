# Spec: `src/janus/cli/generate.py`
- **Label:** ESTABLISHED
- **Phase:** 47
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
CLI: generate text.

## Interface (inputs → outputs, with shapes where applicable)
--checkpoint --prompt

## Required tests (CPU, tiny config)
Smoke run.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
