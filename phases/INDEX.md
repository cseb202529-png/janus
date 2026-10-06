# Phase Index (update status as phases pass)
| # | Phase | Status |
|---|---|---|
| 00 | [Project Specification](00_project_specification.md) | delivered — awaiting Director approval |
| 01 | [Environment](01_environment.md) | delivered — awaiting Director approval |
| 02 | [Repository Bootstrap](02_repository_bootstrap.md) | delivered — awaiting Director approval |
| 03 | [Tokenizer](03_tokenizer.md) | not started |
| 04 | [Baseline 1M Model](04_baseline_1m_model.md) | not started |
| 05 | [Automated Parameter Accounting](05_automated_parameter_accounting.md) | not started |
| 06 | [Testing System](06_testing_system.md) | not started |
| 07 | [Tiny Overfit](07_tiny_overfit.md) | not started |
| 08 | [GQA](08_gqa.md) | not started |
| 09 | [MLA](09_mla.md) | not started |
| 10 | [SSM](10_ssm.md) | not started |
| 11 | [Hybrid Backbone](11_hybrid_backbone.md) | not started |
| 12 | [Meta Tokens](12_meta_tokens.md) | not started |
| 13 | [MoE](13_moe.md) | not started |
| 14 | [Adaptive Routing](14_adaptive_routing.md) | not started |
| 15 | [Thought Engine](15_thought_engine.md) | not started |
| 16 | [TRM](16_trm.md) | not started |
| 17 | [External Memory](17_external_memory.md) | not started |
| 18 | [Verifier](18_verifier.md) | not started |
| 19 | [Janus-10M](19_janus-10m.md) | not started |
| 20 | [Janus-30M](20_janus-30m.md) | not started |
| 21 | [Ablation Pipeline](21_ablation_pipeline.md) | not started |
| 22 | [Data Engineering](22_data_engineering.md) | not started |
| 23 | [Dataset Versioning](23_dataset_versioning.md) | not started |
| 24 | [Final Tokenizer](24_final_tokenizer.md) | not started |
| 25 | [125M Parameter Design](25_125m_parameter_design.md) | not started |
| 26 | [Final Model Assembly](26_final_model_assembly.md) | not started |
| 27 | [Pretraining](27_pretraining.md) | not started |
| 28 | [Training Monitor](28_training_monitor.md) | not started |
| 29 | [Checkpoint Management](29_checkpoint_management.md) | not started |
| 30 | [Knowledge Distillation](30_knowledge_distillation.md) | not started |
| 31 | [Teacher Instruction Data](31_teacher_instruction_data.md) | not started |
| 32 | [GRA](32_gra.md) | not started |
| 33 | [Feedback-Driven Distillation](33_feedback-driven_distillation.md) | not started |
| 34 | [Multi-Step KD](34_multi-step_kd.md) | not started |
| 35 | [Curriculum Training](35_curriculum_training.md) | not started |
| 36 | [Instruction Tuning](36_instruction_tuning.md) | not started |
| 37 | [Preference Optimization](37_preference_optimization.md) | not started |
| 38 | [GRPO](38_grpo.md) | not started |
| 39 | [Gradient-Balanced GRPO](39_gradient-balanced_grpo.md) | not started |
| 40 | [BREAD](40_bread.md) | not started |
| 41 | [Model Merging](41_model_merging.md) | not started |
| 42 | [Adapter System](42_adapter_system.md) | not started |
| 43 | [Stream Adapter](43_stream_adapter.md) | not started |
| 44 | [NeSyCD](44_nesycd.md) | not started |
| 45 | [Soup of Experts](45_soup_of_experts.md) | not started |
| 46 | [Low-Bit Experiment](46_low-bit_experiment.md) | not started |
| 47 | [Inference](47_inference.md) | not started |
| 48 | [Chat Engine](48_chat_engine.md) | not started |
| 49 | [API](49_api.md) | not started |
| 50 | [UI](50_ui.md) | not started |
| 51 | [Evaluation](51_evaluation.md) | not started |
| 52 | [Model Comparison](52_model_comparison.md) | not started |
| 53 | [Regression Testing](53_regression_testing.md) | not started |
| 54 | [Failure Analysis](54_failure_analysis.md) | not started |
| 55 | [Model Card](55_model_card.md) | not started |
| 56 | [Technical Paper](56_technical_paper.md) | not started |

## Legacy build-order mapping
Spec → repo → env → config → logging → seed → tokenizer → data → baseline → param counter → tests → tiny overfit → GQA → RoPE → SwiGLU → MLA → SSM → hybrid → meta tokens → MoE → routing → thought → TRM → verifier → memory → KV cache → 10M → 30M → ablations → 125M config → final tokenizer → dataset → pretrain → checkpoint → validation → KD → teacher data → GRA → FDD → MSKD → instruct → preference → GRPO → balanced GRPO → merging → LoRA → memory training → eval → failure analysis → inference → FastAPI → Gradio → benchmarks → quantization → docs → model card → report → release.
