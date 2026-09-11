# AEGIS Foundation Model Training

This directory contains the reproducible post-training pipeline for AEGIS. It does **not** claim that a new foundation model has already been trained; it provides the code and dataset contract needed to train one from an authorized base model.

## Strategy

1. Start from a strong open-weight instruct model.
2. Build a high-quality, licensed/authorized corpus covering reasoning, coding, tool use, real-estate operations, digital marketing, automation, and defensive cybersecurity.
3. Run supervised fine-tuning (SFT) with TRL + PEFT/LoRA.
4. Evaluate against a held-out benchmark before publishing a checkpoint.
5. Add preference optimization only after SFT quality is measured.
6. Serve the resulting adapter/checkpoint through an OpenAI-compatible inference endpoint and register it with the AEGIS provider router.

TRL supports conversational datasets and PEFT adapters, making this workflow practical without retraining every parameter of a large model. See the official documentation before running a large job.

## Dataset contract

Training examples are JSONL records using the chat format:

```json
{"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

Keep only data you are authorized to use. Remove secrets, credentials, personal data that is not required, and unsafe operational instructions.

## Training

```bash
pip install -r training/requirements.txt
python training/train_sft.py --model Qwen/Qwen3-4B-Instruct --data data/aegis_train.jsonl --output artifacts/aegis-sft
```

For a local smoke test:

```bash
python training/train_sft.py --model Qwen/Qwen3-0.6B --data data/aegis_train.jsonl --output artifacts/smoke --max-samples 100
```

The default configuration uses LoRA so the first experiments are affordable and reproducible. Full-model training is a later stage, not the starting point.

## Evaluation gate

A model is not considered an AEGIS release merely because training completes. A release candidate must pass:

- general instruction following
- tool-call correctness
- coding tests
- factuality checks
- cybersecurity defensive/authorized-use tests
- refusal and permission-boundary tests
- regression tests against the previous release

Record metrics in `training/evals/` and publish the exact base model, dataset version, training configuration, and evaluation results with each release.
