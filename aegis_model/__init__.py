"""AEGIS language-model family: tokenizer, Transformer, configs, training, generation."""

from .model import AEGISConfig, AEGISForCausalLM
from .tokenizer import ByteTokenizer
from .configs import AEGIS_1T_CONFIG, estimate_parameter_count

__all__ = [
    "AEGISConfig",
    "AEGISForCausalLM",
    "ByteTokenizer",
    "AEGIS_1T_CONFIG",
    "estimate_parameter_count",
]
