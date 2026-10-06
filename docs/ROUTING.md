# Routing Specification
Two router types: (1) MoE expert router (top-k, load balancing, capacity); (2) Adaptive computation router (choice among ATTENTION, SSM, MOE, THOUGHT, MEMORY).
Requirements: router outputs logged per layer; auxiliary load-balancing loss; compute-budget regularizer; collapse detection (entropy, expert utilization); fallback to fixed path via config; defined precedence between the two routers; tests for top-k correctness, determinism, gradient flow, and collapse.
