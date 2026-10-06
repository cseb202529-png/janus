# Spec: `src/janus/training/losses.py`
- **Label:** ESTABLISHED
- **Phase:** 04
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Cross-entropy LM loss plus aux losses (MoE balance, routing budget, verifier).

## Interface (inputs → outputs, with shapes where applicable)
logits,labels→scalar + components dict.

## Required tests (CPU, tiny config)
Masking of pad/meta tokens; matches manual CE.

## Notes / edge cases / risks
Training component. Config-driven, resumable, logs JSONL.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
