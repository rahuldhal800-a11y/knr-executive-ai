## 2023-09-07 - Lazy loading heavy ML/Data Dependencies
**Learning:** Initializing heavy dependencies (like `openai`, `chromadb`, and `duckduckgo_search`) at the module level or during class instantiation causes massive startup bottlenecks (taking ~2.88s).
**Action:** Always encapsulate these heavy imports and client initializations within `@property` getters so they are only loaded when explicitly needed, reducing startup time to ~0.06s.
