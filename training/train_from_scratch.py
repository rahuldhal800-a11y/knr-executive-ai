"""Train the AEGIS decoder-only Transformer from random initialization.

This is real pretraining code: it does not download or initialize a third-party
LLM. It trains the AEGIS architecture from tokenized text supplied by the user.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Dataset

from aegis_model import AEGISConfig, AEGISForCausalLM, ByteTokenizer


class PackedText(Dataset):
    def __init__(self, path: str, tokenizer: ByteTokenizer, seq_len: int) -> None:
        records: list[str] = []
        source = Path(path)
        if source.suffix == ".jsonl":
            for line in source.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                if "messages" in row:
                    records.append("\n".join(f"{m['role']}: {m['content']}" for m in row["messages"]))
                elif "text" in row:
                    records.append(str(row["text"]))
        else:
            records.append(source.read_text(encoding="utf-8"))
        ids: list[int] = []
        for text in records:
            ids.extend(tokenizer.encode(text, add_bos=True, add_eos=True))
        self.data = torch.tensor(ids, dtype=torch.long)
        self.seq_len = seq_len

    def __len__(self) -> int:
        return max(0, (len(self.data) - 1) // self.seq_len)

    def __getitem__(self, idx: int):
        start = idx * self.seq_len
        x = self.data[start : start + self.seq_len]
        y = self.data[start + 1 : start + self.seq_len + 1]
        if len(x) < self.seq_len:
            x = torch.nn.functional.pad(x, (0, self.seq_len - len(x)), value=ByteTokenizer.PAD)
            y = torch.nn.functional.pad(y, (0, self.seq_len - len(y)), value=-100)
        y[x == ByteTokenizer.PAD] = -100
        return x, y


def main() -> None:
    p = argparse.ArgumentParser(description="Pretrain AEGIS from random initialization")
    p.add_argument("--data", required=True)
    p.add_argument("--output", default="artifacts/aegis-small")
    p.add_argument("--steps", type=int, default=1000)
    p.add_argument("--seq-len", type=int, default=512)
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--grad-accumulation", type=int, default=4)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="auto")
    args = p.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)
    device = "cuda" if args.device == "auto" and torch.cuda.is_available() else ("mps" if args.device == "auto" and torch.backends.mps.is_available() else ("cpu" if args.device == "auto" else args.device))

    tokenizer = ByteTokenizer()
    cfg = AEGISConfig(max_seq_len=args.seq_len)
    model = AEGISForCausalLM(cfg).to(device)
    dataset = PackedText(args.data, tokenizer, args.seq_len)
    if len(dataset) == 0:
        raise RuntimeError("Training corpus is too small for one sequence. Add more authorized text.")
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, drop_last=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)
    scaler = torch.amp.GradScaler("cuda", enabled=device == "cuda")

    model.train()
    step = 0
    optimizer.zero_grad(set_to_none=True)
    while step < args.steps:
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=device == "cuda"):
                loss = model(x, y)["loss"] / args.grad_accumulation
            scaler.scale(loss).backward()
            if (step + 1) % args.grad_accumulation == 0:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad(set_to_none=True)
            step += 1
            if step % 50 == 0:
                ppl = math.exp(min(20.0, float(loss * args.grad_accumulation)))
                print(f"step={step} loss={loss.item() * args.grad_accumulation:.4f} ppl={ppl:.2f} device={device}")
            if step >= args.steps:
                break

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    torch.save({"config": vars(cfg), "state_dict": model.state_dict()}, out / "model.pt")
    tokenizer.save(out / "tokenizer.json")
    (out / "README.txt").write_text(f"AEGIS model trained from random initialization. Parameters: {model.parameter_count():,}. Steps: {step}. Device: {device}.\n", encoding="utf-8")
    print(f"saved {out / 'model.pt'} ({model.parameter_count():,} parameters)")


if __name__ == "__main__":
    main()
