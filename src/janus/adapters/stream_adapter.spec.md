# Spec: `src/janus/adapters/stream_adapter.py`
- **Label:** EXPERIMENTAL
- **Phase:** 43
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Controlled runtime adaptation.

## Interface (inputs → outputs, with shapes where applicable)
-

## Required tests (CPU, tiny config)
Adaptation, stability, forgetting, rollback.

## Notes / edge cases / risks
V2; later.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
