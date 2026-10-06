# Planned Ablation Ladder
| ID | Change | Hypothesis | Success metric |
|---|---|---|---|
| E0 | dense transformer baseline | reference | val loss |
| E1 | + GQA | lower KV memory, similar quality | loss, KV size |
| E2 | + MLA | lower KV memory further | loss, KV size, speed |
| E3 | + SSM (hybrid) | better long-context efficiency | loss, throughput |
| E4 | + meta tokens | better conditioning | loss, tasks |
| E5 | + MoE (2–4 experts) | more capacity per FLOP | loss at matched active params |
| E6 | + adaptive routing | compute savings at equal quality | quality vs FLOPs |
| E7 | + Thought Engine | reasoning gain | reasoning/math evals |
| E8 | + TRM | iterative improvement | evals vs steps |
| E9 | + external memory | retention/knowledge | memory evals |
Run at 30M first. Each: ≥3 seeds before any claim.
