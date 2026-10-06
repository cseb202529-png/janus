# Spec: `src/janus/tokenizer/special_tokens.py`
- **Label:** ESTABLISHED
- **Phase:** 03
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Single definition of special tokens: PAD, BOS, EOS, UNK, system/user/assistant markers, meta-token placeholders, memory markers.

## Interface (inputs → outputs, with shapes where applicable)
Constants and ID map.

## Required tests (CPU, tiny config)
IDs stable; no collisions.

## Notes / edge cases / risks
Changing IDs is a breaking change.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
