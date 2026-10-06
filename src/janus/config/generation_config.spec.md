# Spec: `src/janus/config/generation_config.py`
- **Label:** ESTABLISHED
- **Phase:** 47
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Sampling config.

## Interface (inputs → outputs, with shapes where applicable)
YAML → GenerationConfig (temperature, top_k, top_p, repetition_penalty, max_new_tokens, stop tokens).

## Required tests (CPU, tiny config)
Validation of ranges.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
