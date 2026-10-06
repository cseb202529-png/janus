# Spec: `src/janus/model/router.py`
- **Label:** EXPERIMENTAL
- **Phase:** 13,14
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Routers: MoE expert router and adaptive computation router (ATTENTION/SSM/MOE/THOUGHT/MEMORY).

## Interface (inputs → outputs, with shapes where applicable)
[B,T,D]→routing weights/indices + aux losses + stats.

## Required tests (CPU, tiny config)
Determinism; gradient flow; collapse detection; fixed-path fallback.

## Notes / edge cases / risks
See docs/ROUTING.md. Define precedence with MoE router.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
