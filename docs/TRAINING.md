# Training Pipeline
Stages: tokenizer → pretraining (next-token) → knowledge distillation (logit, hidden-state, multi-step, feedback-driven) → instruction tuning → preference optimization (length-normalized) → experimental GRPO → merging/adapters.
Pretraining requirements: AdamW, warmup, cosine schedule, grad clipping, mixed precision auto-detect (BF16 preferred, FP16 with scaler, FP32 fallback), grad accumulation, checkpoint/resume (model, optimizer, scheduler, tokenizer, config, RNG, metrics), validation loop, JSONL logging, experiment ID.
Curriculum order: basic language → high-quality text → knowledge → coding → math → reasoning → instructions → preference data.
Always start with a tiny-run config. Never start with the full configuration.
Checkpoint names: `checkpoint_000100`, `checkpoint_000500`, `checkpoint_001000`, ...
Dashboard (Phase 28) shows: train/val loss, perplexity, LR, grad norm, tokens/sec, VRAM, GPU util, expert routing, memory retrieval, time.
