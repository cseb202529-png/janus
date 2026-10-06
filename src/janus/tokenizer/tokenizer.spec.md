# Spec: `src/janus/tokenizer/tokenizer.py`
- **Label:** ESTABLISHED
- **Phase:** 03
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Tokenizer wrapper (SentencePiece/BPE-based) with encode/decode and versioning.

## Interface (inputs → outputs, with shapes where applicable)
encode(str)→List[int]; decode(List[int])→str; batch variants; vocab_size; version string; save/load.

## Required tests (CPU, tiny config)
Round trip encode→decode equals original on diverse text (unicode, code, whitespace); deterministic; special tokens never split; version recorded.

## Notes / edge cases / risks
Tokenizer version stored in every checkpoint and eval result.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
