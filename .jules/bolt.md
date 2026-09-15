## 2024-05-24 - Lazy-loading ML dependencies
**Learning:** Initializing heavy libraries like `openai`, `chromadb`, and `duckduckgo_search` at module import time blocks application startup in CLI tools. Moving these initializations to `@property` getters drops orchestrator initialization from ~3.5s to ~0.06s.
**Action:** Always lazy-load heavy machine learning or data dependencies in CLI scripts and agents to prevent startup bottlenecks. Delay import statements and client initialization until the specific tool or method is invoked.
