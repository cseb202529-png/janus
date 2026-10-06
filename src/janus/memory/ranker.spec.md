# Spec: `src/janus/memory/ranker.py`
- **Label:** EXPERIMENTAL
- **Phase:** 17
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Re-rank by relevance, recency, score.

## Interface (inputs → outputs, with shapes where applicable)
items→ordered items.

## Required tests (CPU, tiny config)
Ordering rules.

## Notes / edge cases / risks
-

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
