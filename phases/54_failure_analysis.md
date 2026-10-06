# Phase 54 — Failure Analysis

**Goal:** Reports on hallucination, repetition, instruction, reasoning, math, coding, memory retrieval, context forgetting, expert collapse

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 53 passed its gate (see `phases/INDEX.md`).

## Deliverables
- reports/failure_*.md

## Gate (must pass before Phase 55)
- reports generated from real outputs
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
