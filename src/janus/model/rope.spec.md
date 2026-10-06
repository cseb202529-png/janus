# Spec: `src/janus/model/rope.py`
- **Label:** ESTABLISHED
- **Phase:** 04
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Rotary position embeddings, supports cached offsets and MLA's decoupled rope part if needed.

## Interface (inputs → outputs, with shapes where applicable)
q,k [B,H,T,Dh], positions→rotated q,k.

## Required tests (CPU, tiny config)
Relative-position property test; offset equals full-sequence result.

## Notes / edge cases / risks
Model component. Document every tensor shape; support the config flag; expose param count.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
