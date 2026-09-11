"""Run a trained AEGIS checkpoint locally."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from aegis_model import AEGISConfig, AEGISForCausalLM, ByteTokenizer


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--tokens", type=int, default=128)
    p.add_argument("--temperature", type=float, default=0.8)
    args = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
    ckpt = torch.load(args.checkpoint, map_location=device, weights_only=False)
    model = AEGISForCausalLM(AEGISConfig(**ckpt["config"])).to(device)
    model.load_state_dict(ckpt["state_dict"])
    tokenizer = ByteTokenizer.load(Path(args.checkpoint).with_name("tokenizer.json"))
    prompt = tokenizer.encode(args.prompt)
    ids = torch.tensor([prompt], dtype=torch.long, device=device)
    out = model.generate(ids, max_new_tokens=args.tokens, temperature=args.temperature)
    print(tokenizer.decode(out[0].tolist()[len(prompt):]))


if __name__ == "__main__":
    main()
