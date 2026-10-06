# Phase 00 — Project Specification

**Goal:** Produce architecture doc, requirements, repo structure, coding/testing standards, config design, parameter-budget strategy, experiment system

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
None.

## Deliverables
- docs/specification.md
- docs/ARCHITECTURE.md reviewed
- parameter budget plan

## Gate (must pass before Phase 01)
- Director approves specification
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
