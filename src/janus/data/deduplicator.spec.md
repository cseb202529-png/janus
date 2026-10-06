# Spec: `src/janus/data/deduplicator.py`
- **Label:** ESTABLISHED
- **Phase:** 22
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Exact and near-duplicate removal.

## Interface (inputs → outputs, with shapes where applicable)
stream→stream + stats.

## Required tests (CPU, tiny config)
Exact dup removed; near-dup (e.g. MinHash-style) detected; stable.

## Notes / edge cases / risks
Data pipeline stage. Deterministic, streaming-friendly, logs statistics, records provenance per docs/DATA_POLICY.md.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
