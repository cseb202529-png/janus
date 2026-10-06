# Spec: `src/janus/tokenizer/train_tokenizer.py`
- **Label:** ESTABLISHED
- **Phase:** 03,24
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Train tokenizer on a corpus at a given vocab size (16K/24K/32K/48K/64K).

## Interface (inputs → outputs, with shapes where applicable)
corpus paths, vocab_size → tokenizer artifact + stats (tokens per char, code efficiency, coverage).

## Required tests (CPU, tiny config)
Training on tiny corpus works; artifact loads.

## Notes / edge cases / risks
Phase 24 picks size by efficiency, parameter budget, language coverage, code handling.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
