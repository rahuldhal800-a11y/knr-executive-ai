"""Production-scale AEGIS model configurations.

The 1T preset is a *model specification*. It is intentionally not instantiated
by default because a dense trillion-parameter model requires distributed GPU
training/inference infrastructure.
"""

from __future__ import annotations

from dataclasses import replace

from .model import AEGISConfig

# Dense decoder-only Transformer:
# d_model=16,384, 320 layers, 128 heads, MLP ratio=4, vocab=65,536,
# context=4,096. With tied input/output embeddings this is exactly
# 1,031,954,006,016 trainable parameters in the current implementation.
AEGIS_1T_CONFIG = AEGISConfig(
    vocab_size=65_536,
    max_seq_len=4_096,
    d_model=16_384,
    n_heads=128,
    n_layers=320,
    mlp_ratio=4,
    dropout=0.0,
)


def estimate_parameter_count(cfg: AEGISConfig) -> int:
    """Return the exact parameter count for the current tied-embedding model."""
    d = cfg.d_model
    # token embedding + positional embedding + final LayerNorm
    total = cfg.vocab_size * d + cfg.max_seq_len * d + 2 * d
    # Each block: two LayerNorms + QKV + output projection + two MLP projections.
    per_block = 4 * d + 4 * d * d + 2 * cfg.mlp_ratio * d * d
    return total + cfg.n_layers * per_block


def validate_1t_target() -> None:
    count = estimate_parameter_count(AEGIS_1T_CONFIG)
    if count < 1_000_000_000_000:
        raise AssertionError(f"1T target missed: {count:,}")


def with_context_length(context_length: int) -> AEGISConfig:
    """Create a 1T configuration with a different positional context length."""
    if context_length < 1:
        raise ValueError("context_length must be positive")
    return replace(AEGIS_1T_CONFIG, max_seq_len=context_length)
