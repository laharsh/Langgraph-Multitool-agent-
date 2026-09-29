# Project 2 close-out — tracking

> Governance product story + workflow benchmark. See [docs/WORKFLOWS.md](docs/WORKFLOWS.md).

## Checklist

### Product & eval

- [x] Workflow-based `benchmark/tasks.json` (12 tasks — expand toward 50 if needed)
- [x] `benchmark/grader.py` — numeric + required-tools checks
- [x] Governance tables in `seed_db.py` (`ai_systems`, `compliance_findings`)
- [x] MCP tool server — `python -m src.mcp_tools_server` ([docs/MCP.md](docs/MCP.md))
- [ ] Run full `python benchmark/run_benchmark.py` → paste `by_workflow` rates in README
- [ ] Optional: SmolAgents + [docs/COMPARISON.md](docs/COMPARISON.md)

### Demo & docs

- [x] Cross-link P1 ↔ P2 ([INTEGRATION.md](../rag-eval-platform/docs/INTEGRATION.md))
- [x] [P1_P2_PRODUCT_STORY.md](../projects-plan/P1_P2_PRODUCT_STORY.md)
- [ ] Record Loom: P1 `/ask` → P2 `/chat` or CLI with `tool_calls`
- [ ] Resume bullets (workflow names, not raw % without context)

### GitHub

- [ ] Public repo(s), `.env` gitignored

## Done when

- [ ] Full benchmark run saved; you can explain each workflow in an interview
- [ ] 2-min demo video linked in README
