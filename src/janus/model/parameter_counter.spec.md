# Spec: `src/janus/model/parameter_counter.py`
- **Label:** ESTABLISHED
- **Phase:** 05
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Automated parameter accounting per module.

## Interface (inputs → outputs, with shapes where applicable)
model→{total, trainable, active_per_token, per_module, memory_estimate}.

## Required tests (CPU, tiny config)
Matches analytic counts; MoE active vs total; CLI prints table.

## Notes / edge cases / risks
CLI: python -m janus.cli.inspect

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
