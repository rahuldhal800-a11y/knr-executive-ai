## 2024-05-24 - Lazy-loading ML Dependencies
**Learning:** Large machine learning or data dependencies (like `openai`, `chromadb`, and `duckduckgo_search`) can cause significant startup bottlenecks in CLI scripts and multi-agent systems when imported synchronously at the top level.
**Action:** Always lazy-load heavy dependencies. Delay import statements and client initialization until the specific tool or method is actually invoked, for example by using Python properties.
