# KNR AEGIS AI ⚡

**AEGIS — Agentic Executive & General Intelligence System**

An open, extensible agent platform for research, coding, content, automation, real-estate operations, and defensive cybersecurity. The project combines multi-model routing, tools, memory, device capability controls, and a reproducible model post-training pipeline.

> **Status:** AEGIS v1 is an agent platform. The custom model training pipeline is now in the repository, but a new foundation model has **not** been trained yet.

## Why AEGIS

The goal is not to build another chatbot. The goal is to build a measurable agent system that can:

- plan multi-step digital work;
- use tools and maintain task state;
- route requests across authorized model providers;
- fall back to a local model when hosted capacity is unavailable;
- learn domain behavior through controlled post-training;
- expose specialized skills for coding, marketing, operations, and defensive security;
- connect to registered devices through explicit capability grants;
- produce auditable results rather than opaque background actions.

## Current architecture

```text
                         ┌─────────────────────┐
                         │      User Goal       │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │  AEGIS Orchestrator │
                         └──────────┬──────────┘
                                    ↓
             ┌──────────────────────┼──────────────────────┐
             ↓                      ↓                      ↓
        Planner / Agent         Memory / State        Policy Engine
             ↓                      ↓                      ↓
        Tool Registry          Knowledge Base       Capability ACL
             └──────────────────────┼──────────────────────┘
                                    ↓
                           Multi-Model Router
                 ┌──────────────┬──────────────┬──────────────┐
                 ↓              ↓              ↓              ↓
             Hosted A        Hosted B       Local Model   AEGIS Model
                                    ↓
                             Execution + Audit
```

## Foundation model track

`training/` contains the first reproducible SFT pipeline. It uses Hugging Face TRL + PEFT/LoRA so we can start with parameter-efficient experiments, evaluate them, and only then scale training. TRL supports conversational SFT and tool-calling datasets; PEFT reduces the number of parameters that need to be trained. See the official references in `training/README.md`.

```bash
pip install -r training/requirements.txt
python training/train_sft.py \
  --model Qwen/Qwen3-0.6B \
  --data data/aegis_train.jsonl \
  --output artifacts/aegis-smoke \
  --max-samples 100
```

The long-term model program is:

**Data → SFT → evaluation → preference optimization → specialized adapters → serving → router integration → continuous evaluation.**

Only authorized/licensed datasets should enter the training corpus.

## Agent capabilities

- 🧠 multi-step planning and execution
- 🔀 multi-provider routing and fallback
- 💾 persistent memory
- 🌐 web research
- 💻 coding and filesystem workflows
- 📣 digital marketing/content workflows
- 🏢 real-estate operations workflows
- 🛡️ defensive cybersecurity analysis
- 📱 consent-based device capability adapters
- 📊 model/provider status and discovery

## Security model

AEGIS is designed to be powerful **without treating authorization as optional**. Device actions require registration and explicit capability grants. Cybersecurity skills are scoped to defensive and authorized work. Provider fallback never bypasses quotas, authentication, or access controls.

## Build toward a top-tier open-source project

Quality matters more than a GitHub star claim. The project roadmap prioritizes:

1. deterministic tests and CI;
2. benchmark/evaluation harness;
3. high-quality authorized training corpus;
4. model adapters and specialized agents;
5. observability and audit trails;
6. documented APIs and integrations;
7. secure repository configuration;
8. reproducible releases and model cards;
9. real-world task benchmarks;
10. community contribution standards.

GitHub recommends README, contribution guidance, security controls, Dependabot, secret scanning/push protection, and code scanning for serious repositories.

## Contributing

See `CONTRIBUTING.md` and `SECURITY.md`. Every new tool should define its inputs, permissions, failure modes, and tests.

## License

Add the project's chosen open-source license before public release.
