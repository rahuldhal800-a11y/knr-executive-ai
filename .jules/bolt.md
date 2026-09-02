## 2024-05-14 - Lazy Load Heavy CLI Dependencies
**Learning:** Top-level imports of heavy libraries (like `chromadb` and `openai` via orchestrator modules) in a CLI app block the initial UI rendering, causing a multi-second startup delay.
**Action:** Always defer importing heavy dependencies in CLI tools until *after* the initial user prompt is displayed, ideally hidden behind a loading spinner during the first command execution.
