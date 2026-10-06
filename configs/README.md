# Configs (to be written as YAML by AI)
| File to create | Contents |
|---|---|
| `model_1m.yaml` | baseline dev model, all experimental flags false |
| `model_10m.yaml` | full architecture validation |
| `model_30m.yaml` | ablation scale |
| `model_125m.yaml` | final, dims from Phase 25 solver |
| `training_tiny.yaml` | CPU-runnable tiny training |
| `training_pretrain.yaml` | full pretraining |
| `data_tiny.yaml`, `data_full.yaml` | data pipeline settings |
| `generation_default.yaml` | sampling defaults |
| `experiments/E*.yaml` | per-experiment configs |
| `architecture_registry.yaml` | models and components registry (see below) |
Rule: nothing hard-coded in source; every key documented with type, default, valid range.
