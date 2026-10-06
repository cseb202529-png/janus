# Phase 47 — Inference

**Goal:** Greedy, temperature, top-k, top-p, repetition penalty, stop tokens, KV cache, streaming

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 46 passed its gate (see `phases/INDEX.md`).

## Deliverables
- inference/*

## Gate (must pass before Phase 48)
- cached==uncached
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
