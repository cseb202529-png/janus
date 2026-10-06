# Phase 52 — Model Comparison

**Goal:** BASE vs +KD vs +reasoning vs +memory vs +adapters; no "feels smarter"

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 51 passed its gate (see `phases/INDEX.md`).

## Deliverables
- comparison report

## Gate (must pass before Phase 53)
- numbers-based table
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
