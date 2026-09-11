"""Distributed training entry point for the AEGIS 1T specification.

This launcher deliberately refuses to run a trillion-parameter dense model on a
single ordinary process. Use a distributed PyTorch/FSDP/DeepSpeed environment
with sufficient accelerator memory and checkpoint storage.
"""

from __future__ import annotations

import argparse

from aegis_model.configs import AEGIS_1T_CONFIG, estimate_parameter_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print the 1T training specification without allocating the model")
    args = parser.parse_args()

    params = estimate_parameter_count(AEGIS_1T_CONFIG)
    print("AEGIS 1T distributed training specification")
    print(f"parameters: {params:,}")
    print(f"layers: {AEGIS_1T_CONFIG.n_layers}")
    print(f"hidden size: {AEGIS_1T_CONFIG.d_model}")
    print(f"attention heads: {AEGIS_1T_CONFIG.n_heads}")
    print(f"context length: {AEGIS_1T_CONFIG.max_seq_len}")
    print(f"vocabulary: {AEGIS_1T_CONFIG.vocab_size}")
    if not args.dry_run:
        raise RuntimeError(
            "The 1T model is specified but not allocated by this launcher. "
            "Configure distributed FSDP/ZeRO training and adequate GPU memory before execution."
        )


if __name__ == "__main__":
    main()
