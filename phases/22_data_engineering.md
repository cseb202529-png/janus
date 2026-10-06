# Phase 22 — Data Engineering

**Goal:** Collector, cleaner, normalizer, quality scorer, dedup, language filter, contamination, safety filter, shards, packer. Director chooses sources, verifies licenses

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 21 passed its gate (see `phases/INDEX.md`).

## Deliverables
- data/*

## Gate (must pass before Phase 23)
- pipeline runs on tiny data; provenance recorded
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
