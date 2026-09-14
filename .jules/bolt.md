## 2025-02-23 - Lazy Loading Heavy ML and Data Dependencies
**Learning:** Initializing heavy dependencies (like `openai`, `chromadb`, and `duckduckgo_search`) at the module level or in constructor defaults introduces significant startup bottlenecks, slowing down any script or CLI utility that imports them even if it doesn't immediately use those features.
**Action:** Always lazy-load heavy machine learning or data dependencies in CLI scripts and agents. Use Python `@property` decorators to delay import statements and client initialization until the specific tool or method is actually invoked.
