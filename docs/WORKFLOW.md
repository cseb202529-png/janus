# Human + AI Workflow
Daily: open project → pick ONE task → send task request (`templates/TASK_REQUEST.md`) → AI writes code → run tests → send full traceback on failure (`templates/ERROR_REPORT.md`) → accept/reject patch → **commit + push → next task.**

**Push rule (binding):** every commit goes to `origin` = `https://github.com/cseb202529-png/janus.git`, branch `main`, after *every* unit of work (phase gate, module + tests, doc update). No work stays local-only; never force-push. Full policy: `docs/DELIVERY.md`.
Cross-review: AI-A implements, AI-B reviews adversarially, AI-C writes tests, AI-A fixes, Director runs final tests. A model must not be the only reviewer of its own work.
Save important sessions to `research/ai_sessions/`.
Never send: "Build the whole model." Send: "Implement phase NN" with the phase file.
