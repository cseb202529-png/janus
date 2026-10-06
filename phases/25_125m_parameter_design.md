# Phase 25 — 125M Parameter Design

**Goal:** Automatically solve hidden size, layers, heads, KV heads, FFN, experts, SSM dims, embedding dims to ≈125M

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 24 passed its gate (see `phases/INDEX.md`).

## Deliverables
- solver script
- configs/model_125m.yaml

## Gate (must pass before Phase 26)
- counter reports 125M ±3%
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
