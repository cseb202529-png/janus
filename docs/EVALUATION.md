# Evaluation
Measure: perplexity, knowledge, reasoning, math, coding, instruction following, memory, context retention, latency, throughput, safety.
Each result JSON records: model checkpoint, tokenizer version, dataset version, config, seed, score.
Comparisons: BASE vs +KD vs +reasoning vs +memory vs +adapters. Benchmark report table columns: Model, Params, Tokens, Loss, PPL, Reasoning, Math, Code, Memory, Latency, VRAM.
Failure analysis reports: hallucination, repetition, instruction failure, reasoning failure, math errors, coding errors, memory retrieval errors, context forgetting, expert collapse.
