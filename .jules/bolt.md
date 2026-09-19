## 2023-10-27 - Heavy Imports Slowing Startup
**Learning:** Top-level imports of heavy ML/Search libraries (`chromadb`, `duckduckgo_search`, `openai`) caused the orchestrator to take ~2.5s just to initialize.
**Action:** Use Python `@property` decorators to lazily load and initialize the heavy modules/clients only when they are accessed.
