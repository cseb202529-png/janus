# Phase 11 — Hybrid Backbone

**Goal:** Attention and SSM blocks alternating e.g. A,S,A,S,A,S

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 10 passed its gate (see `phases/INDEX.md`).

## Deliverables
- hybrid_block
- transformer pattern config

## Gate (must pass before Phase 12)
- hybrid trains on tiny; causality holds
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
