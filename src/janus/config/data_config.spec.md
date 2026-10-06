# Spec: `src/janus/config/data_config.py`
- **Label:** ESTABLISHED
- **Phase:** 02
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Data pipeline config.

## Interface (inputs → outputs, with shapes where applicable)
YAML → DataConfig (sources, filters thresholds, dedup params, shard size, packing length, tokenizer ref).

## Required tests (CPU, tiny config)
Validation; round trip.

## Notes / edge cases / risks
Sources reference dataset records.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
