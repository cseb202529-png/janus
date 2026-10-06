# Spec: `src/janus/model/gqa.py`
- **Label:** ESTABLISHED
- **Phase:** 08
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Grouped-query attention (n_kv_heads ≤ n_heads), causal.

## Interface (inputs → outputs, with shapes where applicable)
x [B,T,D]→[B,T,D]; kv cache optional.

## Required tests (CPU, tiny config)
n_kv_heads==n_heads equals MHA; causality; param formula; cache equals no-cache.

## Notes / edge cases / risks
Benchmark vs MHA (speed, memory, loss).

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
