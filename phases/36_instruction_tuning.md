# Phase 36 — Instruction Tuning

**Goal:** Janus-125 BASE → Janus-125-INSTRUCT

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 35 passed its gate (see `phases/INDEX.md`).

## Deliverables
- instruct checkpoint

## Gate (must pass before Phase 37)
- instruction eval improves
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
