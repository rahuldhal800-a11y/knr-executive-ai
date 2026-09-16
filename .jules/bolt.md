## 2024-05-18 - CLI Startup Bottlenecks from Heavy ML Dependencies
**Learning:** In command-line applications like KNR Executive AI that import heavy ML packages (e.g., openai, chromadb), loading these modules globally causes severe startup latency even when those tools aren't immediately used.
**Action:** Use Python `@property` decorators on classes to lazy-load dependencies (like OpenAI, chromadb) only when the specific tool or method is invoked. This avoids loading heavy libraries at script startup.
