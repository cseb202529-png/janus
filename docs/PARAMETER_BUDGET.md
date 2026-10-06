# Parameter Budget (provisional — Phase 25 solver decides)
Target total ≈ 125M (±3%). Provisional allocation for planning only:
| Group | Provisional share |
|---|---|
| Token embeddings (tied with LM head) | 15–20% |
| Attention (GQA/MLA) | 15–20% |
| SSM blocks | 10–15% |
| FFN / MoE experts | 35–45% |
| Routers, meta tokens | ≤2% |
| Thought Engine + TRM + Verifier | 5–8% |
| Memory controller/encoders | 2–4% |
| Norms and misc | ≤1% |
Rules: dimensions are solved by an automated search using `parameter_counter.py`; report **total** and **active-per-token** parameters separately for MoE; tokenizer sizes tested: 16K, 24K, 32K, 48K, 64K; embedding share must be justified at each size. Never claim 125M unless counted.
