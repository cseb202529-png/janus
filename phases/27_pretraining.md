# Phase 27 — Pretraining

**Goal:** Next-token objective: AdamW, warmup, cosine, clipping, mixed precision, accumulation, checkpointing, validation, logging

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 26 passed its gate (see `phases/INDEX.md`).

## Deliverables
- training/*
- configs/training_pretrain.yaml

## Gate (must pass before Phase 28)
- run levels L1→L6 passed in order
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
