# Phase 29 — Checkpoint Management

**Goal:** Save model, optimizer, scheduler, tokenizer, config, RNG, metrics; checkpoint_000100 style

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 28 passed its gate (see `phases/INDEX.md`).

## Deliverables
- training/checkpoint

## Gate (must pass before Phase 30)
- resume reproduces
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
