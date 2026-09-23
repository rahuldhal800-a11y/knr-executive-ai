## 2024-09-23 - FlashAttention via is_causal
**Learning:** PyTorch's `F.scaled_dot_product_attention` can automatically use highly optimized memory-efficient backends (like FlashAttention) when `is_causal=True` is provided instead of an explicit lower-triangular boolean mask.
**Action:** Always prefer `is_causal=True` over creating and passing explicit mask tensors in causal self-attention modules to save memory and increase inference/training speed.
