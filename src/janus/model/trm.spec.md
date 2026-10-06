# Spec: `src/janus/model/trm.py`
- **Label:** EXPERIMENTAL
- **Phase:** 16
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Recursive refinement with halting: refine→refine→verify→continue/stop.

## Interface (inputs → outputs, with shapes where applicable)
state→refined state, steps_used.

## Required tests (CPU, tiny config)
Max steps bound; halting determinism; gradient through steps (documented truncation if used).

## Notes / edge cases / risks
Interaction with KV cache must be defined.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
