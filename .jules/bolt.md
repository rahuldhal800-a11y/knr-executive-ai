## 2026-09-20 - Lazy Loading Heavy Dependencies in CLI Tools
**Learning:** Initializing heavy dependencies like `openai`, `chromadb`, and `duckduckgo_search` synchronously during global or top-level class instantiation causes significant startup bottlenecks in CLI tools (~3s wait before prompt appears).
**Action:** Always wrap heavy, potentially unused imports and their client initializations in Python `@property` decorators or lazy-loading patterns to instantiate them only upon the first functional invocation.
