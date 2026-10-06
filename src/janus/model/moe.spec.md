# Spec: `src/janus/model/moe.py`
- **Label:** ESTABLISHED
- **Phase:** 13
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Mixture of experts FFN with top-k routing and load-balancing loss. Start 2–4 experts.

## Interface (inputs → outputs, with shapes where applicable)
[B,T,D]→[B,T,D] + aux_loss.

## Required tests (CPU, tiny config)
Top-k correctness; load balance; dropped-token handling; active vs total params; gradient to selected experts only.

## Notes / edge cases / risks
Not 64 experts in a 125M model.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
