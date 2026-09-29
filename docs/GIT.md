# Git — no AI attribution on commits

See the same steps in [RAG_Eval docs/GIT.md](https://github.com/laharsh/RAG_Eval/blob/main/docs/GIT.md) (or copy `core.hooksPath` setup below).

```powershell
git config core.hooksPath .githooks
git commit -m "Initial commit: LangGraph governance operations agent."
git remote add origin https://github.com/laharsh/Langgraph-Multitool-agent-.git
git push -u origin main
```

Cursor Settings → **Agents → Attribution** → off for commit/PR attribution.
