# Spec: `src/janus/model/memory.py`
- **Label:** EXPERIMENTAL
- **Phase:** 17
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
In-model interface to external memory (read-in via cross-attention/gated fusion).

## Interface (inputs → outputs, with shapes where applicable)
[B,T,D] + retrieved [B,K,D]→[B,T,D].

## Required tests (CPU, tiny config)
Flag off == baseline output; shape; gating.

## Notes / edge cases / risks
Pairs with src/janus/memory/.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
