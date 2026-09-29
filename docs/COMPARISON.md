# LangGraph vs SmolAgents (comparison)

> Fill this after running `python benchmark/run_benchmark.py` on all tasks.

## Setup

| Framework | Entry point | Tools |
|-----------|-------------|-------|
| **LangGraph** | `run_agent` / `POST /chat` | sql_query, calculator, web_search, knowledge_search |
| **SmolAgents** | `src/smolagents_demo.py` (optional) | Same tools wrapped for SmolAgents |

## Results (update with real numbers)

Benchmark uses **workflow grading** (`content` + `required_tools` + optional `expected_numeric`).  
See `benchmark_results.json` field `by_workflow`.

| Metric | LangGraph | SmolAgents |
|--------|-----------|------------|
| Tasks run | 12 | _optional_ |
| Overall pass rate | _TBD_ | _TBD_ |
| `regulatory_brief` pass | _TBD_ | _TBD_ |
| Avg latency (s) | _TBD_ | _TBD_ |

## Notes

- LangGraph gives explicit **state graph** + **tool_calls** log (good for demos).
- SmolAgents is faster to prototype; less control over multi-step routing.
- Both use the same Groq model in `.env` for fair comparison.

## Commands

```bash
python benchmark/run_benchmark.py
# Optional SmolAgents run — then paste scores above
```
