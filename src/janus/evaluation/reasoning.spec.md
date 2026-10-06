# Spec: `src/janus/evaluation/reasoning.py`
- **Label:** ESTABLISHED
- **Phase:** 51
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Reasoning evals.

## Interface (inputs → outputs, with shapes where applicable)
-

## Required tests (CPU, tiny config)
-

## Notes / edge cases / risks
Evaluator. Output structured JSON with checkpoint, tokenizer version, dataset version, config, seed, score.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
