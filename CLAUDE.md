# AGENTS.md — Mandatory Rules for Every AI Agent

You are working on **Janus**. The human is Project Director / tester / decision maker. You implement.

## 1. Source of truth
`PROJECT_SPEC.md` overrides everything. If a phase file or module spec conflicts with it, stop and report the conflict. Do not guess.

## 2. Workflow (never skip)
REQUIREMENT → DESIGN → REVIEW → CODE → UNIT TEST → DEBUG → INTEGRATION TEST → BENCHMARK → ACCEPT/REJECT → NEXT.
Work on **one phase / one subsystem at a time**. Never "build the whole model".

## 3. Hard rules
1. Never fabricate implementation details, citations, or benchmark numbers.
2. Never silently change architecture, APIs, or file layout.
3. No placeholders, `TODO` stubs, or pseudocode in production modules.
4. Every module ships with tests; tests must pass before moving on.
5. Document input/output tensor shapes for every transformation.
6. Every architectural change reports parameter-count and memory impact.
7. All hyperparameters come from YAML configs; nothing hard-coded (device, CUDA, paths included).
8. Experimental components sit behind a config flag (ablation switch).
9. Never delete or weaken tests, remove failing components, or hide warnings to get green.
10. Never claim a result without running it. Never claim "125M" unless the counter says so.
11. Never load pretrained weights into the base model. Distillation teachers are allowed only in distillation phases.
12. Label every component **ESTABLISHED** or **EXPERIMENTAL**. Do not call combinations of known techniques "novel".
13. If two techniques conflict, do not combine silently: explain and create separate experiment variants.
14. Before editing an existing file, inspect its current interfaces. Do not rewrite unrelated files.
15. State every assumption explicitly.
16. Tests must run on CPU with tiny configs.

## 4. Required footer on every coding response
```
FILES CREATED:
FILES MODIFIED:
DEPENDENCIES:
TEST COMMAND:
TEST RESULT:
PARAMETER IMPACT:
MEMORY IMPACT:
NEXT DEPENDENCY:
ASSUMPTIONS:
KNOWN LIMITATIONS:
```

## 5. When blocked
Stop, state the blocker, propose options. Do not work around by weakening requirements.

## 6. Hallucination control
- "Guarantees better performance" → cite the experiment or retract.
- "Novel" → name prior architectures that combine the same parts.
- "Correct" → show shapes and passing tests.
