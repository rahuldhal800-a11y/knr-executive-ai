# KNR Executive AI — AEGIS

AEGIS is being developed as an independent AI system with its own model architecture, tokenizer, training pipeline, evaluation layer, tools, memory, and deployment stack.

## What is now in this repository

### AEGIS model from scratch

`aegis_model/` contains a compact decoder-only Transformer implemented in PyTorch. It starts from **random initialization**; it does not use OpenAI, Anthropic, Gemini, or another hosted LLM for its model weights.

- byte-level tokenizer
- causal self-attention
- Transformer blocks
- tied input/output embeddings
- causal language-model loss
- local autoregressive generation
- configurable model size and sequence length

The default research configuration is intentionally small so that the architecture can be tested before scaling.

### Training

`training/train_from_scratch.py` is the actual pretraining entry point. It reads an authorized text/JSONL corpus, initializes AEGIS randomly, trains it with next-token prediction, and writes a checkpoint.

Install:

```bash
pip install -r training/requirements-from-scratch.txt
```

Train a small research checkpoint:

```bash
python training/train_from_scratch.py \
  --data data/aegis_train.jsonl \
  --output artifacts/aegis-small \
  --steps 1000
```

Run a checkpoint:

```bash
python scripts/aegis_generate.py \
  --checkpoint artifacts/aegis-small/model.pt \
  --prompt "AEGIS:"
```

The included dataset is a small development dataset, **not enough to produce a capable general-purpose LLM**. A serious model requires a much larger, legally authorized corpus, substantially more compute, tokenizer research, distributed training, and rigorous evaluation.

## Existing AEGIS systems

The repository also contains the provider router, agent/tool layer, defensive cybersecurity skills, consent-based device capability layer, post-training/LoRA pipeline, evaluation benchmark, and mobile PWA work. These systems are complementary to the from-scratch model; they do not make the current checkpoint a frontier model.

## Verification

The model package has unit smoke tests in `tests/test_aegis_model.py`, executed by `.github/workflows/test-aegis-model.yml`.

A model is not declared successful merely because training starts or code compiles. Track loss/perplexity, held-out validation, instruction following, coding, tool use, factuality, safety, and regression metrics before calling a checkpoint an AEGIS release.

## Data and safety

Only train on data you are authorized to use. Do not commit credentials, secrets, unnecessary personal data, or copyrighted material without the required rights. Keep tool and device actions behind explicit authorization and capability boundaries.
