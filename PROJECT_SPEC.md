# PROJECT_SPEC.md — Janus (Source of Truth)

## Identity
- Name: **Janus**. Version line: v0.1 → v1.0 (Janus-125 BASE) → v2.0.
- Type: decoder-only autoregressive LM, ~125M parameters (tolerance ±3%), text only (V1).
- Language: Python 3.x, PyTorch. Config: YAML. Data: JSON/JSONL. DB: SQLite. Shell: Bash. Tests: pytest.
- Package: `src/janus/`. CLI entry: `python -m janus.cli.<tool>`.

## Scale ladder
Janus-1M (dev) → Janus-10M (architecture validation) → Janus-30M (ablations) → Janus-125M (final).

## Components
| Component | Status | Notes |
|---|---|---|
| Decoder-only transformer, RMSNorm, RoPE, SwiGLU, weight tying | ESTABLISHED | baseline |
| GQA | ESTABLISHED | compare vs MHA |
| MLA (latent KV) | ESTABLISHED (adapted) | do not assume it wins |
| SSM (Mamba-style) | ESTABLISHED | base SSM before any variant |
| Hybrid Attention+SSM backbone | ESTABLISHED idea, EXPERIMENTAL config | alternating layers |
| Learnable meta tokens | EXPERIMENTAL | ablate on/off |
| MoE (2–4 experts first) | ESTABLISHED | load balancing required |
| Adaptive computation router | EXPERIMENTAL (main novel-ish component) | paths: ATTENTION, SSM, MOE, THOUGHT, MEMORY |
| Thought Engine | EXPERIMENTAL | hidden refinement; no exposed chain-of-thought required |
| TRM recursive refinement | EXPERIMENTAL | refine→refine→verify→continue/stop |
| External memory (SQLite → vector index later) | EXPERIMENTAL | |
| Verifier | EXPERIMENTAL | arithmetic, logic, consistency, structured output |
| BitMamba / low-bit | EXPERIMENTAL, last | |
| BREAD, StreamAdapter, GRPO variants, NeSyCD, Soup of Experts | EXPERIMENTAL, V2 | not core to pretraining |

## Parameter policy
Target ~125M. Per-module counts tracked (see `docs/PARAMETER_BUDGET.md`). Phase 25 solves dimensions automatically with the counter, never by guessing.

## Data policy
Legal and auditable only: source, license, size, token count, filters, date, hash recorded per dataset version (`docs/DATA_POLICY.md`). The Director approves sources and licenses.

## Training policy
AdamW, warmup + cosine, grad clipping, mixed precision (auto-detect BF16/FP16), grad accumulation, resumable checkpoints, validation, structured logs, experiment IDs. Always tiny-run before full run. Scale 100 → 1K → 10K examples → corpora.

## Evaluation policy
Structured JSON results recording checkpoint, tokenizer version, dataset version, config, seed, score. Regression suite on every model version. No "it feels smarter".

## "From scratch" definition
Director designs architecture/strategy; AI writes code; random init; no pretrained Janus weights; distillation is a separate, labeled stage (`Janus-125-BASE` vs `Janus-125-DISTILLED`).

## V1 scope
Text LM, hybrid backbone, GQA, MLA, RoPE, RMSNorm, SwiGLU, weight tying, SSM, MoE, meta tokens, adaptive routing, Thought Engine, basic TRM, external memory, distillation, evaluation, inference, API, UI.
## V1 excludes
Image/video/speech/multimodal, distributed infrastructure, custom CUDA kernels, custom hardware.

## Versioning
v0.1 tokenizer · v0.2 baseline · v0.3 GQA · v0.4 MLA · v0.5 SSM · v0.6 hybrid · v0.7 MoE · v0.8 routing · v0.9 thought engine · v0.10 memory · v1.0 Janus-125 BASE · v1.1 KD · v1.2 instruct · v1.3 preference · v1.4 reasoning · v2.0 advanced research.

## Done condition (V1)
See `docs/DEFINITION_OF_DONE.md`.
