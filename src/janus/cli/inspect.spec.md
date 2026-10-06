# Spec: `src/janus/cli/inspect.py`
- **Label:** ESTABLISHED
- **Phase:** 05
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
CLI: python -m janus.cli.inspect prints total/trainable params, memory, per-module counts.

## Interface (inputs → outputs, with shapes where applicable)
--config

## Required tests (CPU, tiny config)
Output format test.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
