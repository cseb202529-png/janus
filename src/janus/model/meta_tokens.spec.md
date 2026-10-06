# Spec: `src/janus/model/meta_tokens.py`
- **Label:** EXPERIMENTAL
- **Phase:** 12
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Learnable continuous meta tokens (memory/reasoning/planning/verification roles).

## Interface (inputs → outputs, with shapes where applicable)
n_meta × D parameters; inserted into sequence.

## Required tests (CPU, tiny config)
Causal mask correctness; length accounting; removed from outputs/labels.

## Notes / edge cases / risks
Ablate with/without.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
