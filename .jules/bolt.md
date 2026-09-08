## 2024-06-12 - Heavy ML/Data Dependencies Initialization
**Learning:** Initializing heavy dependencies (like `openai`, `chromadb`, and `duckduckgo_search`) synchronously during class instantiation in CLI scripts blocks the main thread and significantly increases startup time (e.g., from ~0.2s to ~3s).
**Action:** Always lazy-load heavy machine learning or data dependencies in CLI scripts and agents. Delay import statements and client initialization using Python `@property` decorators or inside the specific tool/method invocation to prevent startup bottlenecks.
