"""Discover public Hugging Face text-generation models for manual/provider configuration.

This does not assume that a discovered model has free hosted inference. Hugging
Face model pages can be public while inference still requires a provider or
local runtime. The script only discovers metadata; it never downloads or runs
untrusted model code automatically.
"""
import argparse
import json
import urllib.parse
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    params = urllib.parse.urlencode({"pipeline_tag": "text-generation", "sort": "downloads", "direction": "-1", "limit": args.limit})
    url = "https://huggingface.co/api/models?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "KNR-AEGIS-AI/1.0"})
    with urllib.request.urlopen(req, timeout=20) as response:
        data = json.load(response)
    print(json.dumps([
        {"id": x.get("id"), "downloads": x.get("downloads"), "likes": x.get("likes")}
        for x in data
    ], indent=2))


if __name__ == "__main__":
    main()
