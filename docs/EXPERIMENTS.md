# Experiments
Registry: `experiments/E001/ ...`, each with `config.yaml, result.json, notes.md, metrics.csv` (see `experiments/_template/`).
Ablation ladder: E0 dense → E1 +GQA → E2 +MLA → E3 +SSM → E4 +meta tokens → E5 +MoE → E6 +adaptive routing → E7 +Thought Engine → E8 +TRM → E9 +memory.
Rules: one change per experiment; fixed seeds (≥3 for claims); same data/tokens budget per comparison; report parameter-matched comparisons; keep failures. A component survives only if it beats the baseline at matched params/compute.
Runner: `scripts/run_experiment.py --config configs/<file>.yaml` → load config → build model → count params → train → evaluate → save results.
