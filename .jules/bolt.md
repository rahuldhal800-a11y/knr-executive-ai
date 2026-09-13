## 2024-05-17 - Lazy Loading AI/Data Dependencies
**Learning:** Initializing heavy libraries like `openai`, `chromadb`, and `duckduckgo_search` at module level creates a significant startup bottleneck (~2.5s locally) because they are loaded before the orchestrator is even started.
**Action:** Use the `@property` decorator pattern to lazily import and initialize these clients only when they are first accessed. This keeps the initial application import fast (~0.06s).
