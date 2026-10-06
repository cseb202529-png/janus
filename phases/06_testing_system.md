# Phase 06 — Testing System

**Goal:** Unit, shape, gradient, numerical, save/load tests for tokenizer, embeddings, RMSNorm, RoPE, attention, FFN, model, loss, generation

## Read first
`AGENTS.md`, `PROJECT_SPEC.md`, `docs/ARCHITECTURE.md`, and the module specs under `src/janus/` that match the deliverables below.

## Prerequisite
Phase 05 passed its gate (see `phases/INDEX.md`).

## Deliverables
- tests/unit/*
- tests/integration/*

## Gate (must pass before Phase 07)
- full suite green on CPU
- All tests green on CPU; `docs/QUALITY_GATES.md` satisfied.
- Parameter and memory impact reported.

## Rules for this phase
- Implement only this phase. Do not touch unrelated modules.
- Experimental parts behind config flags; state assumptions; no placeholders.
- If the gate fails: STOP, use `prompts/02_DEBUGGER.md`, fix, re-run. Do not weaken tests.

## Required response footer
See `AGENTS.md` §4.
