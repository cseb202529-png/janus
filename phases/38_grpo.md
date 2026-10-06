# Phase 38 — GRPO

**Goal:** Only after base, instruct, eval: prompt→multiple generations→reward→relative comparison→optimization

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 37 passed its gate (see `phases/INDEX.md`).

## Deliverables
- training/grpo

## Gate (must pass before Phase 39)
- stable vs baseline
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
