# Phase 23 — Dataset Versioning

**Goal:** dataset_v001… with source, license, size, tokens, filters, date, hash

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 22 passed its gate (see `phases/INDEX.md`).

## Deliverables
- datasets/dataset_v001.md

## Gate (must pass before Phase 24)
- hash verifies
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
