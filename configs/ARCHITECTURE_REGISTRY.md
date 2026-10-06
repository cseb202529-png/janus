# architecture_registry.yaml spec
`models:` janus_1m, janus_10m, janus_30m, janus_125m (each → config file, param target, status).
`components:` gqa, mla, ssm, moe, meta_tokens, adaptive_routing, thought_engine, trm, memory, verifier (each → module path, label ESTABLISHED/EXPERIMENTAL, config flag, required tests, ablation id).
`variants:` the eight ModelFactory variants with their flag sets.
