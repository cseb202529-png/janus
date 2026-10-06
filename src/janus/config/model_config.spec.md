# Spec: `src/janus/config/model_config.py`
- **Label:** ESTABLISHED
- **Phase:** 02
- **Config flag:** see `configs/` (experimental modules MUST be switchable off)

## Purpose
Dataclass-based model configuration loaded from YAML, with validation.

## Interface (inputs → outputs, with shapes where applicable)
YAML path/dict → ModelConfig (vocab_size, d_model, n_layers, n_heads, n_kv_heads, ffn_dim, max_seq_len, component flags, MoE/SSM/TRM/memory sub-configs).

## Required tests (CPU, tiny config)
Load valid YAML; reject invalid (heads not dividing d_model, kv_heads not dividing heads); round trip to dict; defaults documented.

## Notes / edge cases / risks
All component flags default to false except baseline pieces.

## Acceptance criteria
- Implements the interface exactly; no placeholders.
- Documented shapes; parameter count method reconciles with `model/parameter_counter.py`.
- All listed tests pass; no NaN/Inf; deterministic under fixed seed.
- Response ends with the footer from `AGENTS.md`.

## Out of scope
Anything not listed above. Do not modify unrelated modules.
