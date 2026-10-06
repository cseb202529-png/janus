# Spec: `src/janus/model/model.py`
- **Label:** ESTABLISHED
- **Phase:** 04–26
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Top-level Janus model assembled by ModelFactory from config flags.

## Interface (inputs → outputs, with shapes where applicable)
ids [B,T], optional memory/cache→logits [B,T,V], aux dict (losses, routing stats).

## Required tests (CPU, tiny config)
Forward/backward; flags on/off; variants; save/load; report params/config/tokenizer/checkpoint version.

## Notes / edge cases / risks
ModelFactory must support all 8 variants in docs/ARCHITECTURE.md.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
