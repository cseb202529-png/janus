# Phase 02 — Repository Bootstrap

**Goal:** Create directories, __init__.py, pyproject, requirements, README, config system, logging, seed

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 01 passed its gate (see `phases/INDEX.md`).

## Deliverables
- package skeleton
- config/*
- utils/logging
- utils/seed
- utils/device

## Gate (must pass before Phase 03)
- import janus works; config tests pass
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
