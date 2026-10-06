# Spec: `src/janus/adapters/lora.py`
- **Label:** ESTABLISHED
- **Phase:** 41,42
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
LoRA adapters.

## Interface (inputs → outputs, with shapes where applicable)
base layer + rank r→adapted layer.

## Required tests (CPU, tiny config)
Zero-init equals base; merge/unmerge exact.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
