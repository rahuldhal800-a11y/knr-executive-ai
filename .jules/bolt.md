## 2024-05-10 - Lazy Load Heavy ML/Search Dependencies
**Learning:** Initializing large libraries like `openai`, `chromadb`, and `duckduckgo_search` globally or during class `__init__` in a multi-agent AI system causes massive startup bottlenecks (e.g., 3.09s to initialize `MultiAgentOrchestrator`).
**Action:** Always wrap heavy ML or external service clients in property methods (lazy loading) to delay their import and instantiation until exactly when the tool or service is first invoked. This reduces CLI/service startup time to fractions of a second (e.g., 0.06s).
