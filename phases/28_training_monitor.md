# Phase 28 — Training Monitor

**Goal:** Dashboard: loss, val loss, ppl, lr, grad norm, tokens/sec, VRAM, GPU util, expert routing, memory retrieval, time

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 27 passed its gate (see `phases/INDEX.md`).

## Deliverables
- dashboard

## Gate (must pass before Phase 29)
- metrics visible live
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
