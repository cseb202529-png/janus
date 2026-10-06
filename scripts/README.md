# Scripts (specs for AI to implement)
| Script | Purpose |
|---|---|
| `check_environment.py` | report Python, PyTorch, CUDA availability, GPU, VRAM, BF16/FP16, device |
| `run_experiment.py --config X` | load config → build model → count params → train → evaluate → save |
| `build_dataset.py` | run data pipeline, write dataset version record |
| `train_tokenizer.py` | train tokenizer for given vocab size |
| `count_parameters.py` | per-module parameter report |
| `make_report.py` | generate experiment/benchmark report |
| `export_checkpoint.py` | package checkpoint + config + tokenizer |
