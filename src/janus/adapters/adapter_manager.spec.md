# Spec: `src/janus/adapters/adapter_manager.py`
- **Label:** EXPERIMENTAL
- **Phase:** 42
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Register, select, route among adapters (reasoning, coding, math, dialogue, retrieval).

## Interface (inputs → outputs, with shapes where applicable)
task→adapter.

## Required tests (CPU, tiny config)
Switching correctness; no leakage between adapters.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
