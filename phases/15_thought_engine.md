# Phase 15 — Thought Engine

**Goal:** Hidden reasoning module, soft cognitive modules, iterative refinement; no exposed chain-of-thought required

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 14 passed its gate (see `phases/INDEX.md`).

## Deliverables
- model/thought_engine

## Gate (must pass before Phase 16)
- k=0 identity; cost reported
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
