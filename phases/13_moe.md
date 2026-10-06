# Phase 13 — MoE

**Goal:** Router, experts, top-k, load balancing; start with 2–4 experts

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 12 passed its gate (see `phases/INDEX.md`).

## Deliverables
- model/moe
- model/router

## Gate (must pass before Phase 14)
- balance loss works; active vs total params reported
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
