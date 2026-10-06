# Phase 46 — Low-Bit Experiment

**Goal:** LAST: normal precision→quantization→low-bit research; compare quality, size, speed, memory

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 45 passed its gate (see `phases/INDEX.md`).

## Deliverables
- quantized variants

## Gate (must pass before Phase 47)
- comparison table
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
