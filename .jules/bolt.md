## 2024-05-16 - Lazy Loading Heavy Dependencies in Tools and LLM Client
**Learning:** Initializing heavy dependencies like `openai`, `chromadb`, and `duckduckgo_search` synchronously during class instantiation causes unnecessary startup bottlenecks, especially for CLI applications or when these tools are not immediately invoked.
**Action:** Use Python `@property` decorators to lazy-load these dependencies. This defers the import and initialization overhead until the specific client is accessed for the first time, significantly improving the startup time of the application.
