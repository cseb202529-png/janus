# Janus Specification (Phase 00 deliverable)

- **Status:** draft for Director approval (Phase 00 gate).
- **Source of truth:** `PROJECT_SPEC.md` overrides this document on any conflict.
- **Reviewed:** `docs/ARCHITECTURE.md` reviewed against `PROJECT_SPEC.md` — **no conflicts found**;
  dataflow, layer description, variant list and watchlist here are consistent with it.
- **Labels:** every component is marked **ESTABLISHED** or **EXPERIMENTAL** per `AGENTS.md` §3.12.

## 1. Scope (V1)

Decoder-only autoregressive text LM, ~125M parameters (±3%, verified by counter — never by
assumption). Random init, no pretrained Janus weights. Excluded: multimodal, distributed
infrastructure, custom CUDA kernels.

## 2. Module graph

```
janus/
├── config/       model_config, training_config, data_config, generation_config  [ESTABLISHED]
├── utils/        device, logging (JSONL), seed, metrics, profiling, reproducibility  [ESTABLISHED]
├── tokenizer/    tokenizer, special_tokens, tokenizer_utils, train_tokenizer  [ESTABLISHED]
├── data/         loader, deduplicator, filters, pack, shard, dataloader  [ESTABLISHED]
├── model/        ← core architecture
│   ├── embeddings, rmsnorm, rope, lm_head (tied)          [ESTABLISHED]
│   ├── attention (MHA), gqa                               [ESTABLISHED]
│   ├── mla (latent KV)                                    [ESTABLISHED, adapted]
│   ├── ssm (base Mamba-style)                             [ESTABLISHED]
│   ├── hybrid_block (A/S alternation + FFN)               [ESTABLISHED idea, EXPERIMENTAL config]
│   ├── swiglu                                              [ESTABLISHED]
│   ├── moe (2–4 experts, load balancing)                  [ESTABLISHED]
│   ├── meta_tokens                                         [EXPERIMENTAL]
│   ├── router (adaptive computation)                      [EXPERIMENTAL — main novel-ish component]
│   ├── thought_engine, trm                                [EXPERIMENTAL]
│   ├── verifier                                           [EXPERIMENTAL]
│   ├── kv_cache, cross_layer_kv, bitmamba                 [EXPERIMENTAL / last]
│   ├── transformer (block stack), model (ModelFactory)    [ESTABLISHED]
│   └── parameter_counter                                  [ESTABLISHED]
├── memory/       database (SQLite), embeddings, retriever, ranker, controller  [EXPERIMENTAL]
├── training/     optimizer, scheduler, losses, trainer, checkpoint,
│                 mixed_precision, gradient_accumulation, pretraining, kd, ...  [ESTABLISHED]
├── distillation/ teacher, generator, reviewer, adjudicator, gra, fdd, mskd  [EXPERIMENTAL, labeled stage]
├── evaluation/   perplexity, math, reasoning, memory, regression, ...  [ESTABLISHED]
├── inference/    generation, kv_cache, sampler, batching, chat  [ESTABLISHED]
├── adapters/     lora, stream_adapter, adapter_manager    [EXPERIMENTAL, V2-heavy]
├── cli/          train, generate, evaluate, inspect, benchmark  [ESTABLISHED]
├── api/          FastAPI server                             [ESTABLISHED]
└── ui/           Gradio app                                 [ESTABLISHED]
```

Dependency order (build DAG): `utils → config → tokenizer → data → model/* → training →
memory → distillation → evaluation → inference → api/ui`. Router depends on attention + ssm
+ moe. Thought/TRM/verifier plug into the router paths. Nothing imports upward.

## 3. Tensor dimensions

| Stage | Tensor | Shape | dtype |
|---|---|---|---|
| Input | `ids` | `[B, T]` | int64 |
| Embedding (tied w/ LM head) | `hidden` | `[B, T, D]` | fp32/bf16 |
| Meta tokens (flag) | `meta` | `[B, M, D]` → concat → `[B, T+M, D]` | model dtype |
| RMSNorm (pre-norm ×2/block) | `hidden` | `[B, T, D]` | fp32 for norm |
| Attention Q | `q` | `[B, H, T, d_h]`, `d_h = D / H` | model dtype |
| Attention K/V (GQA) | `k, v` | `[B, H_kv, T, d_h]`, `H_kv ≤ H` | model dtype |
| MLA latent KV | `c_kv` | `[B, T, D_c]` (`D_c < H_kv·d_h`) | model dtype |
| Attention scores | `attn` | `[B, H, T, T]` (+ causal mask), softmax in fp32 | fp32 |
| SSM state | `h` | `[B, D, T]` (selective scan) or recurrent `[B, D]` | fp32 accum |
| SwiGLU FFN | intermediate | `[B, T, F]` (gate, up), out `[B, T, D]` | model dtype |
| MoE | router logits | `[B·T, E]`; expert out `[B, T, D]` | model dtype |
| LM head | `logits` | `[B, T, V]` | fp32 for loss |
| Loss | `loss` | `[]` (scalar) | fp32 |
| Aux dict | routing/load/thought stats | dicts of scalars `[ ]` | fp32 |

Convention: `B` batch, `T` sequence length, `D` model dim, `F` FFN dim, `H` heads,
`H_kv` KV groups, `E` experts, `V` vocab, `M` meta tokens.

## 4. Layer arrangement

1. `ids [B,T]` → token embedding `[B,T,D]` (tied with LM head).
2. Optional meta tokens prepended (flag `meta_tokens`, EXPERIMENTAL): `[B, T+M, D]`.
   Causal-mask and context accounting rules: meta tokens occupy the first M positions.
3. `n_layers` backbone blocks, pre-RMSNorm → residual:
   - pattern from config, e.g. baseline `A,A,A,...`; hybrid `A,S,A,S,...`
   - `A` = attention (MHA or GQA or MLA by flag), `S` = SSM block
   - each followed by FFN: SwiGLU dense, or MoE (flag `moe`)
   - RoPE applied inside attention; RoPE positions cover meta+text tokens.
4. Adaptive router (flag `adaptive_routing`, EXPERIMENTAL): per-token decision among
   `{ATTENTION, SSM, MOE, THOUGHT, MEMORY}`; fixed hybrid is the default, routing enabled
   only behind the flag; compute-budget penalty + collapse monitor required.
5. Thought Engine / TRM (flags): hidden latent refinement loop, verifier-gated, max steps
   from config.
6. Final RMSNorm → tied LM head → `logits [B,T,V]`.

Variants via `ModelFactory` (exactly 8): `JANUS-DENSE, JANUS-GQA, JANUS-MLA, JANUS-HYBRID,
JANUS-HYBRID-MOE, JANUS-HYBRID-THOUGHT, JANUS-HYBRID-MEMORY, JANUS-125`.
Config flags: `attention, gqa, mla, ssm, moe, meta_tokens, adaptive_routing, thought_engine,
trm, memory, verifier` — all default `false` except baseline pieces (`attention`).

## 5. Parameter budget

Full plan in `docs/PARAMETER_BUDGET.md` (provisional shares). Analytical formulas
(verification only via `model/parameter_counter.py` in Phases 05/25 — **no number here is a
claimed count**):

| Group | Formula (tied embeddings) |
|---|---|
| Token embedding + LM head (tied) | `V·D` (untied: `2·V·D`) |
| RMSNorms | `≈ 2·D·L` (+ `D` final) |
| MHA attention/layer | `4·D²` |
| GQA attention/layer | `2·D² + 2·D·(H_kv·d_h)` |
| MLA attention/layer | `D·D_c + D_c² + 2·D_c·(H·d_h) + D²` (simplified) |
| SwiGLU FFN/layer | `3·D·F` |
| MoE FFN (E experts) | `E·3·D·F + D·E` router |
| SSM block/layer | `≈ 3–4·D·(D + N)` state-space params, `N` state dim |
| Router / meta tokens | `≤ 2%` of total (budget rule) |

Solver: Phase 25 searches `(D, L, F, H, H_kv, V, E)` with the counter to hit 125M ±3%.
Tokenizer sizes evaluated: 16K/24K/32K/48K/64K; embedding share justified per size.
Report **total** and **active-per-token** params separately for MoE.

Illustrative planning point only (dense, NOT a claimed count): e.g. `V=32K, D=768, L=12,
F=2048` gives `≈ 110M` by the formulas above; the Phase 25 solver + counter decide the
actual configuration.

## 6. FLOPs and memory estimates (analytical, not measured)

Forward matmul FLOPs per token, dense: `≈ 2·P_non-embed` (from the parameter formulas),
plus attention score/value terms per layer `≈ 4·T·D` (causal halves the score term in
practice: `≈ 2·T·D + 2·T·D`). Sequence-level attention cost `≈ 2·L·T²·D` (QKᵀ) +
`2·L·T²·D` (scores·V), halved by the causal mask.

Memory (planning formulas):
- Weights: `4·P` bytes fp32; `2·P` bytes bf16/fp16 (+ `4·P` fp32 master weights under
  mixed precision → `≈ 8·P` bytes total with optimizer states excluded).
- AdamW states: `≈ 8·P` bytes (m, v in fp32).
- Gradients: `2·P` bf16 or `4·P` fp32.
- Activations (naive, no checkpointing): `≈ B·T·L·c·D` bytes with `c ≈ 10–15`
  tensors/block × dtype size; checkpointing reduces to `≈ B·T·D·√L`-scale.
- KV cache at inference: `2·B·T·L·H_kv·d_h·bytes`.

These are estimates; benchmark numbers come only from Phase 27/51 runs recorded in
`experiments/`.

## 7. Training implications

- AdamW + warmup + cosine, grad clipping, grad accumulation, mixed precision
  (auto-detect BF16/FP16, fp32 loss accumulation), resumable checkpoints, validation,
  JSONL logs, experiment IDs.
- Scale ladder: 100 → 1K → 10K examples → corpora; Janus-1M → 10M → 30M → 125M.
- Tiny CPU run before every full run (`training_tiny.yaml`).

## 8. Inference implications

- KV cache required for decode (`inference/kv_cache`); greedy/temperature/top-k/top-p
  sampling from `GenerationConfig`.
- MoE: active-per-token params ≠ total; memory sized on total.
- TRM refinement invalidates cache segments → cache flush policy per refinement step (see
  watchlist below).
- Memory module reads/writes gated by router; latency budget logged separately.

## 9. Incompatibility watchlist (from ARCHITECTURE.md — each gets a DECISIONS.md note + separate variant)

1. **MLA latent KV vs KV-cache sharing across layers** — latent cache is per-layer; no
   sharing across layers in V1.
2. **SSM state vs adaptive routing** — skipped tokens break recurrent state continuity;
   default: SSM layers always process all tokens; router may not skip SSM inputs (V1 rule).
3. **MoE routing vs adaptive routing** — two routers: MoE router is *inside* the FFN path,
   adaptive router picks the *block type*; precedence: adaptive router first, MoE load
   balancing only over tokens routed to MOE; joint stats logged.
4. **TRM loops vs KV cache** — refinement changes hidden states → invalidate affected
   cache rows; simplest correct policy: full cache flush per refinement step.
5. **Meta tokens vs causal masking / context accounting** — meta tokens occupy positions
   `0..M-1`; `max_seq_len` budget includes them; text length `T ≤ max_seq_len - M`.

## 10. Ablation variants (config-flag driven, EXPERIMENTAL items flagged)

| Variant | What changes |
|---|---|
| JANUS-DENSE | baseline: MHA, dense SwiGLU, no experimental flags |
| JANUS-GQA | GQA on (H_kv < H) |
| JANUS-MLA | MLA latent KV on |
| JANUS-HYBRID | A/S alternating backbone |
| JANUS-HYBRID-MOE | + MoE FFN (E experts, load-balanced) |
| JANUS-HYBRID-THOUGHT | + Thought Engine/TRM |
| JANUS-HYBRID-MEMORY | + external memory |
| JANUS-125 | final assembly, dims from Phase 25 solver |

Per-ablation: one flag changed at a time; each experiment registered under `experiments/`
with config, seed, and result JSON (see `docs/EXPERIMENTS.md`).

## 11. Phase 00 gate checklist

- [x] `docs/specification.md` produced (this doc).
- [x] `docs/ARCHITECTURE.md` reviewed — no conflicts with `PROJECT_SPEC.md`.
- [x] Parameter budget plan present (`docs/PARAMETER_BUDGET.md` §5 above).
- [x] Parameter impact: none (documentation only — 0 new parameters, 0 bytes of tensors).
- [x] Memory impact: none (documentation only).
- [ ] Director approval of specification — **pending Project Director sign-off**.
- Tests: no test suite exists yet (Phase 06 builds it); `pytest` collects 0 tests, exit
  code 5 (no tests) — recorded as N/A, not as a pass of future tests.
