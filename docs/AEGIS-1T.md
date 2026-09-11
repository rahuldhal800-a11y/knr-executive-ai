# AEGIS 1T

AEGIS now has an explicit dense **1,031,954,006,016-parameter** model specification.

## Architecture

| Setting | Value |
|---|---:|
| Parameters | 1,031,954,006,016 |
| Layers | 320 |
| Hidden size | 16,384 |
| Attention heads | 128 |
| MLP ratio | 4x |
| Vocabulary | 65,536 |
| Context | 4,096 tokens |
| Architecture | Decoder-only causal Transformer |
| Embeddings | Tied input/output |

This is an architecture/configuration, not a claim that a 1T checkpoint has already been trained.

A dense 1T model cannot realistically be trained or loaded on a normal laptop/phone. The repository therefore keeps the 1T configuration separate from the small smoke-test model and provides a distributed-training launcher that performs a dry-run specification check before any allocation.

A real 1T training run additionally requires a large authorized dataset, distributed accelerator cluster, optimizer/checkpoint infrastructure, monitoring, evaluation, and substantial compute/storage resources.
