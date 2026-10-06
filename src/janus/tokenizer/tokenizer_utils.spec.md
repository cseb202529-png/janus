# Spec: `src/janus/tokenizer/tokenizer_utils.py`
- **Label:** ESTABLISHED
- **Phase:** 03
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Helpers: padding, truncation, attention-mask building, chat template rendering.

## Interface (inputs → outputs, with shapes where applicable)
lists of ids → padded tensors + masks.

## Required tests (CPU, tiny config)
Shapes; padding side; truncation correctness.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
