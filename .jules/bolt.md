## 2024-05-15 - Lazy-loading ML and data dependencies
**Learning:** Initializing heavy dependencies like `openai`, `chromadb`, and `duckduckgo_search` globally or during class instantiation causes significant startup bottlenecks in CLI scripts.
**Action:** Use property methods or helper methods to lazy-load these dependencies on first access to improve startup time.
