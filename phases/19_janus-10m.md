# Phase 19 — Janus-10M

**Goal:** Build ~10M config validating full architecture

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 18 passed its gate (see `phases/INDEX.md`).

## Deliverables
- configs/model_10m.yaml

## Gate (must pass before Phase 20)
- all components run together; params within tolerance
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
