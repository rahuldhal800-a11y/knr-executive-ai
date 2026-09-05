## 2024-05-09 - Lazy Loading Heavy ML/DB Dependencies
**Learning:** Initializing dependencies like `openai`, `chromadb`, and `duckduckgo_search` at module level or during class instantiation was causing severe startup bottlenecks (taking ~3.6s to start the CLI application). This is critical for CLI responsiveness.
**Action:** Always lazy-load heavy machine learning or data dependencies inside CLI scripts and agents to prevent startup bottlenecks. Delay import statements and client initialization until the specific tool or method is invoked.
