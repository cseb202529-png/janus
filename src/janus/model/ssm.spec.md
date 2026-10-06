# Spec: `src/janus/model/ssm.py`
- **Label:** ESTABLISHED
- **Phase:** 10
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Base state-space (Mamba-style) block: sequential reference path first, then efficient scan.

## Interface (inputs → outputs, with shapes where applicable)
[B,T,D]→[B,T,D]; recurrent state for generation.

## Required tests (CPU, tiny config)
Sequential==parallel; causality; long sequence; gradients; state carry-over.

## Notes / edge cases / risks
Implement base SSM before any BitMamba variant.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
