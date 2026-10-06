# Phase 21 — Ablation Pipeline

**Goal:** Automatic experiment runner E0–E9

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 20 passed its gate (see `phases/INDEX.md`).

## Deliverables
- scripts/run_experiment.py
- experiments/*

## Gate (must pass before Phase 22)
- results table E0–E9 with ≥3 seeds for claims
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
