# Phase 04 — Baseline 1M Model

**Goal:** Embeddings, RMSNorm, RoPE, causal attention, SwiGLU, residuals, LM head, loss. NO MoE, memory, TRM, SSM, GRPO

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 03 passed its gate (see `phases/INDEX.md`).

## Deliverables
- model baseline
- losses
- configs/model_1m.yaml

## Gate (must pass before Phase 05)
- forward/backward pass; basic training works
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
