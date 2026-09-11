import torch

from aegis_model import AEGISConfig, AEGISForCausalLM, ByteTokenizer


def test_tokenizer_roundtrip():
    tok = ByteTokenizer()
    text = "AEGIS ready 🚀"
    ids = tok.encode(text)
    assert tok.decode(ids) == text
    assert tok.VOCAB_SIZE == 260


def test_forward_and_generation():
    cfg = AEGISConfig(max_seq_len=32, d_model=64, n_heads=4, n_layers=2)
    model = AEGISForCausalLM(cfg)
    ids = torch.tensor([[257, 65, 69, 71, 73]])
    out = model(ids, ids)
    assert out["logits"].shape == (1, 5, cfg.vocab_size)
    assert torch.isfinite(out["loss"])
    generated = model.generate(ids, max_new_tokens=3, temperature=0)
    assert generated.shape == (1, 8)
    assert model.parameter_count() > 0
