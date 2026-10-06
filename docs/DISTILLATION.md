# Distillation
Distillation is separate from pretrained weights. Outputs: `Janus-125-BASE` (random init → data) and `Janus-125-DISTILLED`.
Components: teacher interface, data generator, reviewer, adjudicator (GRA: Generator → Reviewer → Adjudicator → Dataset), FDD (Teacher → Student → output → Reviewer → feedback → distill), MSKD (final output, hidden states, intermediates, optional attention patterns).
Instruction categories: explanation, QA, reasoning, summarization, transformation, coding, math, instruction following.
Every distillation run records teacher, prompts, filters, and compares before/after on the eval suite.
