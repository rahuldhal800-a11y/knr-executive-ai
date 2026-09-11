"""Deterministic byte-level tokenizer with a tiny special-token vocabulary."""

from __future__ import annotations

import json
from pathlib import Path


class ByteTokenizer:
    """A dependency-free byte tokenizer suitable for first AEGIS experiments.

    Tokens 0-255 are raw UTF-8 bytes. Special tokens start at 256.
    This is intentionally simple and reproducible; a BPE/SentencePiece tokenizer
    can replace it later without changing the model interface.
    """

    PAD = 256
    BOS = 257
    EOS = 258
    UNK = 259
    VOCAB_SIZE = 260

    def encode(self, text: str, *, add_bos: bool = True, add_eos: bool = False) -> list[int]:
        ids = list(text.encode("utf-8", errors="replace"))
        if add_bos:
            ids.insert(0, self.BOS)
        if add_eos:
            ids.append(self.EOS)
        return ids

    def decode(self, ids: list[int]) -> str:
        data = bytes(i for i in ids if 0 <= i < 256)
        return data.decode("utf-8", errors="replace")

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps({"type": "byte", "vocab_size": self.VOCAB_SIZE}, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "ByteTokenizer":
        json.loads(Path(path).read_text(encoding="utf-8"))
        return cls()
