# Delivery & Git Policy (Director mandate)

**Single remote of record:** every change made to Janus is committed and pushed to:

```
https://github.com/cseb202529-png/janus.git
```

- `origin` = `https://github.com/cseb202529-png/janus.git`, branch `main`.
- **Push after every unit of work** (each phase gate, each module + its tests, each doc update).
  No work stays local-only.
- Commit messages follow the phase/module being delivered, e.g.
  `phase-02: config system, logging, seed, device`.
- Never force-push; never rewrite published history.
- Runtime artifacts (`data/`, `checkpoints/`, `runs/`, `logs/`, `*.pt`, `*.db`) are
  ignored per `.gitignore.md`; their `README.md` placeholders are kept.
- This policy applies to all AI agents working on Janus: the repository above is the
  only destination for commits and pushes.

**Status:** binding policy, set by the Project Director (2026-10-06).
