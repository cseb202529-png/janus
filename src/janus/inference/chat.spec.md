# Spec: `src/janus/inference/chat.py`
- **Label:** ESTABLISHED
- **Phase:** 48
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Chat engine: roles, history, templating, streaming.

## Interface (inputs → outputs, with shapes where applicable)
messages→stream.

## Required tests (CPU, tiny config)
Template round trip.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
