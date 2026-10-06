# Phase 26 — Final Model Assembly

**Goal:** Assemble Janus-125 from surviving components

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 25 passed its gate (see `phases/INDEX.md`).

## Deliverables
- model/model
- ModelFactory
- KV cache

## Gate (must pass before Phase 27)
- forward works; params verified
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
