# KNR AEGIS AI

Autonomous, tool-using executive agent for KNR Integrity and other digital work.

## What changed in v1

- Natural-language multi-step agent loop with a bounded execution budget.
- OpenAI-compatible **multi-provider router**.
- Automatic fallback when a provider reports quota/rate-limit/capacity/timeout failures.
- Local Ollama model as the user's dedicated model slot; no API credit is required for local inference.
- Provider status command (`models`).
- Optional public-model discovery from Hugging Face metadata.
- Existing filesystem, web-search and long-term-memory tools remain the agent's tool surface.

This is an extensible agent core, not a claim of unrestricted autonomy. Tool permissions should be expanded deliberately as new digital-work integrations are added.

## Setup

```bash
git clone https://github.com/rahuldhal800-a11y/knr-executive-ai.git
cd knr-executive-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add at least one provider. For local-only operation, install Ollama and pull a model, then leave `OLLAMA_ENABLED=true`.

For hosted OpenAI-compatible providers, set their API key environment variable and add them to `MODEL_PROVIDERS_JSON`.

Example `.env`:

```env
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
OLLAMA_ENABLED=true
OLLAMA_MODEL=qwen2.5:7b
MODEL_PROVIDERS_JSON=[{"name":"backup","model":"YOUR_MODEL","api_key_env":"BACKUP_API_KEY","base_url":"https://YOUR_PROVIDER/v1"}]
```

## Run

```bash
python3 -m app.main
```

Then give the agent a goal in natural language, for example:

```text
Research five competing real-estate agencies, summarize their positioning, and save the findings to competitor-report.md.
```

Check provider availability:

```text
models
```

## Model discovery

```bash
python3 scripts/discover_models.py --limit 20
```

Discovery only returns public Hugging Face metadata. A public model is **not automatically a free hosted inference endpoint**. To use a model, connect a legitimate compatible provider or run it locally.

## Architecture

```text
User goal
   ↓
ExecutiveManager
   ↓
bounded agent loop
   ├── filesystem tools
   ├── web search
   ├── long-term memory
   └── LLM router
          ├── OpenAI
          ├── configured compatible providers
          └── local Ollama
```

## Important design choice

The router does not bypass exhausted credits or access controls. It detects provider failures and moves to another **configured, authorized** provider. This gives the system resilience without embedding credential theft or service-limit bypasses.
