# Spec: `src/janus/distillation/adjudicator.py`
- **Label:** EXPERIMENTAL
- **Phase:** 32
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Final accept/reject.

## Interface (inputs → outputs, with shapes where applicable)
candidates+reviews→decision.

## Required tests (CPU, tiny config)
Tie-breaking rules.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
