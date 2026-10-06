# JANUS — AI-Native Language Model Project

**Janus** is a research-grade, ~125M-parameter, decoder-only autoregressive language model with a hybrid Attention + SSM backbone, MoE, adaptive computation routing, a Thought Engine, TRM-style recursive refinement, external memory, and a verifier. It is built with an **AI-first workflow**: a human directs, AI agents implement.

> This repository currently contains **only Markdown specifications and folder structure**. No code exists yet. Your job as an AI agent is to turn these specs into code, one phase at a time.

## READ ORDER FOR ANY AI AGENT
1. `AGENTS.md` — operating rules (mandatory)
2. `PROJECT_SPEC.md` — source of truth
3. `docs/ARCHITECTURE.md` — system design
4. `phases/INDEX.md` — find the current phase, then open its phase file
5. The module spec(s) in `src/janus/<area>/` named by that phase
6. `docs/CODING_STANDARDS.md`, `docs/TESTING_STANDARDS.md`
7. `prompts/` — your role prompt

## FOLDER MAP
| Folder | Purpose |
|---|---|
| `src/janus/*` | Each subfolder holds `.spec.md` files: one per future Python module |
| `phases/` | 57 ordered build phases (00–56), each with goal, deliverables, gate |
| `docs/` | Architecture, standards, policies, workflows |
| `prompts/` | Role prompts (architect, coder, debugger, reviewer, ...) |
| `configs/` | Config specs (YAML to be created by AI) |
| `experiments/` | Experiment registry and template |
| `datasets/` | Dataset version records |
| `research/` | Research notes, AI session records |
| `templates/` | Task request / report templates |
| `tests/`, `scripts/` | Test and script specs |
| `reports/`, `runs/`, `logs/`, `checkpoints/`, `data/` | Runtime outputs (see each README) |

## REPOSITORY / DELIVERY
All work is committed and pushed to **https://github.com/cseb202529-png/janus.git** (`origin`, branch `main`) after every unit of work. See `docs/DELIVERY.md`.

## STATUS
Current phase: **00 — Project Specification**. Update `phases/INDEX.md` when a phase passes its gate.
