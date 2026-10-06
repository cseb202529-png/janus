# Spec: `src/janus/data/dataloader.py`
- **Label:** ESTABLISHED
- **Phase:** 22
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Torch-compatible dataloader over shards, resumable.

## Interface (inputs → outputs, with shapes where applicable)
shards→batches [B,T] input_ids, labels, masks.

## Required tests (CPU, tiny config)
Resume gives identical next batch; seed determinism.

## Notes / edge cases / risks
Data pipeline stage. Deterministic, streaming-friendly, logs statistics, records provenance per docs/DATA_POLICY.md.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
