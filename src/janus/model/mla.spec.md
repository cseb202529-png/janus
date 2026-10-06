# Spec: `src/janus/model/mla.py`
- **Label:** ESTABLISHED
- **Phase:** 09
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Multi-head latent attention: low-rank latent KV compression and up-projection.

## Interface (inputs → outputs, with shapes where applicable)
x [B,T,D]→[B,T,D]; caches latent [B,T,Dlatent].

## Required tests (CPU, tiny config)
Causality; cache memory smaller than GQA; cached==uncached; rope handling documented.

## Notes / edge cases / risks
DO NOT ASSUME MLA WINS. Compare baseline, GQA, MLA, GQA+MLA.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
