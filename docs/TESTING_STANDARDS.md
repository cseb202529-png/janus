# Testing Standards
- Framework: pytest. All tests run on **CPU** with tiny configs (hidden ≤ 64, layers ≤ 2, seq ≤ 32).
- Per module: shape test, forward test, backward/gradient test (finite, non-zero where expected), determinism test (same seed → same output), numerical-stability test (large/small inputs, no NaN/Inf), save/load round trip, edge cases (batch 1, seq 1, max seq, padding).
- Causality test for every attention/SSM component: changing a future token must not change earlier outputs.
- Parameter-count test: counted == analytically computed.
- Integration: tokenizer→model→loss; generation with and without KV cache gives identical logits.
- Tiny training test: loss decreases; tiny-overfit test memorizes (Phase 07).
- Regression: previous evaluation suite must not degrade unexpectedly (Phase 53).
- Never delete or weaken a test to pass. A failing test is fixed in code or escalated.
- Test layout mirrors `src/`: `tests/unit/`, `tests/integration/`, `tests/regression/`, `tests/numerical/`.
