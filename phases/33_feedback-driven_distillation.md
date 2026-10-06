# Phase 33 — Feedback-Driven Distillation

**Goal:** Teacher→Student→output→Reviewer→feedback→distill

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 32 passed its gate (see `phases/INDEX.md`).

## Deliverables
- training/fdd

## Gate (must pass before Phase 34)
- compared against plain KD
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
