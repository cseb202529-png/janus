# Phase 51 — Evaluation

**Goal:** Benchmark framework: perplexity, knowledge, reasoning, math, coding, instruction, memory, context retention, latency, throughput

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 50 passed its gate (see `phases/INDEX.md`).

## Deliverables
- evaluation/*

## Gate (must pass before Phase 52)
- JSON results with required fields
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
