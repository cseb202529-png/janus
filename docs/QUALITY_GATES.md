# Quality Gates
| Before | Requirement |
|---|---|
| Merging code | all tests pass |
| Training | model forward works; parameter count verified |
| Long training | tiny training run works; tiny overfit passes |
| Scaling up | parameter count verified; previous scale passed ablations |
| Release | full evaluation + regression + model card + limitations documented |
Run levels: L1 100 examples → L2 1K → L3 10K → L4 small corpus → L5 medium → L6 final.
