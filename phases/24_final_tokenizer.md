# Phase 24 — Final Tokenizer

**Goal:** Test 16K/24K/32K/48K/64K; choose by efficiency, parameter budget, language coverage, code handling

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 23 passed its gate (see `phases/INDEX.md`).

## Deliverables
- tokenizer comparison report

## Gate (must pass before Phase 25)
- Director chooses size
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
