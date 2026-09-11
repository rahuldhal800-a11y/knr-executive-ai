"""Reproducible LoRA SFT entry point for the AEGIS model family."""

from __future__ import annotations

import argparse
from pathlib import Path

from datasets import load_dataset
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--data", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--max-samples", type=int, default=None)
    p.add_argument("--epochs", type=float, default=2.0)
    p.add_argument("--learning-rate", type=float, default=1e-4)
    p.add_argument("--max-length", type=int, default=4096)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--gradient-accumulation", type=int, default=8)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    dataset = load_dataset("json", data_files=args.data, split="train")
    if args.max_samples:
        dataset = dataset.select(range(min(args.max_samples, len(dataset))))

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    lora = LoraConfig(
        r=32,
        lora_alpha=64,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )

    config = SFTConfig(
        output_dir=str(output),
        num_train_epochs=args.epochs,
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation,
        logging_steps=10,
        save_strategy="steps",
        save_steps=100,
        save_total_limit=2,
        max_length=args.max_length,
        packing=True,
        report_to="none",
        gradient_checkpointing=True,
    )

    trainer = SFTTrainer(
        model=args.model,
        args=config,
        train_dataset=dataset,
        peft_config=lora,
    )
    trainer.train()
    trainer.save_model(str(output / "final"))


if __name__ == "__main__":
    main()
