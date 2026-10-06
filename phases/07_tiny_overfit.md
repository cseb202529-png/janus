# Phase 07 — Tiny Overfit

**Goal:** Tiny synthetic dataset; train 1M model until it memorizes

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 06 passed its gate (see `phases/INDEX.md`).

## Deliverables
- synthetic dataset
- configs/training_tiny.yaml
- trainer

## Gate (must pass before Phase 08)
- loss falls strongly and examples memorized. FAIL = STOP EVERYTHING AND DEBUG
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
