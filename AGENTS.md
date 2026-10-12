# Probe session rules

- At the beginning of each new session, run `git pull --ff-only` on `poc/probe`, then read `docs/probe/STATE.md` before continuing. If pull fails, record the real failure; do not reset or force-push.
- Repository remote: `https://github.com/lhmax2010/security_protection.git`; branch: `poc/probe`. Synchronize results only with ordinary `git push`.
- Maintain plans, progress, evidence-backed conclusions, premises requiring PM decisions, and unresolved items in `docs/probe/STATE.md`.
- Keep real REA/tool output under `docs/probe/evidence/`. Preserve original errors and raw Evidence; `.decoded.json` files are projections, not replacements for raw MCP responses.
- Every completed substep needs a STATE update and its own add/commit/push. Use `docs/probe/scripts/checkpoint.py` with explicit paths.
- Native ARM analysis uses Ghidra only. Samples remain unobfuscated and unstripped. External .NET reconstruction and JavaScript recovery must retain their provider provenance and limitations.
- Local dependencies live under ignored `.local-tools/`; use `source docs/probe/scripts/env.sh`. Source samples and generated targets are committed under `docs/probe/samples/`.
- Never fabricate successful analysis or use another tool's results as REA results. Unsupported pyc remains an explicit capability gap.
