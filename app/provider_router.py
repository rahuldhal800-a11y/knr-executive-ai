import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Provider:
    name: str
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    enabled: bool = True


class ModelRouter:
    """OpenAI-compatible model router with quota/rate-limit fallback.

    Providers are configured through MODEL_PROVIDERS_JSON. Each provider must
    expose an OpenAI-compatible chat-completions endpoint. A local Ollama
    provider can be enabled without an API key.
    """

    def __init__(self) -> None:
        self.providers = self._load_providers()
        if not self.providers:
            raise RuntimeError(
                "No model providers configured. Set MODEL_PROVIDERS_JSON or enable OLLAMA."
            )
        self.cooldowns: Dict[str, float] = {}
        self.last_provider: Optional[str] = None

    def _load_providers(self) -> List[Provider]:
        providers: List[Provider] = []
        raw = os.getenv("MODEL_PROVIDERS_JSON", "").strip()
        if raw:
            data = json.loads(raw)
            for item in data:
                providers.append(
                    Provider(
                        name=item["name"],
                        model=item["model"],
                        api_key=item.get("api_key") or os.getenv(item.get("api_key_env", "")),
                        base_url=item.get("base_url"),
                        enabled=item.get("enabled", True),
                    )
                )

        # Convenient environment-based OpenAI provider.
        if os.getenv("OPENAI_API_KEY"):
            providers.insert(
                0,
                Provider(
                    name="openai",
                    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    api_key=os.getenv("OPENAI_API_KEY"),
                    base_url=os.getenv("OPENAI_BASE_URL"),
                ),
            )

        # Local Ollama is the user's own always-available model slot.
        if os.getenv("OLLAMA_ENABLED", "true").lower() == "true":
            providers.append(
                Provider(
                    name="local-ollama",
                    model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
                    api_key="ollama",
                    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                )
            )
        return [p for p in providers if p.enabled]

    @staticmethod
    def _is_transient_or_quota_error(exc: Exception) -> bool:
        text = str(exc).lower()
        markers = (
            "rate limit", "quota", "too many requests", "429", "insufficient_quota",
            "temporarily unavailable", "service unavailable", "timeout", "timed out",
            "overloaded", "capacity"
        )
        return any(marker in text for marker in markers)

    def _client(self, provider: Provider) -> OpenAI:
        kwargs: Dict[str, Any] = {"api_key": provider.api_key or "ollama"}
        if provider.base_url:
            kwargs["base_url"] = provider.base_url
        return OpenAI(**kwargs)

    def chat_completion(self, messages: List[Dict[str, Any]], tools=None, tool_choice="auto"):
        errors = []
        now = time.time()
        ordered = sorted(
            self.providers,
            key=lambda p: self.cooldowns.get(p.name, 0) > now,
        )

        for provider in ordered:
            if self.cooldowns.get(provider.name, 0) > now:
                continue
            try:
                client = self._client(provider)
                kwargs: Dict[str, Any] = {
                    "model": provider.model,
                    "messages": messages,
                }
                if tools:
                    kwargs["tools"] = tools
                    kwargs["tool_choice"] = tool_choice
                response = client.chat.completions.create(**kwargs)
                self.last_provider = provider.name
                return response.choices[0].message
            except Exception as exc:
                errors.append(f"{provider.name}: {exc}")
                if self._is_transient_or_quota_error(exc):
                    # Avoid hammering an exhausted provider during this process.
                    self.cooldowns[provider.name] = time.time() + float(
                        os.getenv("PROVIDER_COOLDOWN_SECONDS", "60")
                    )
                continue

        raise RuntimeError("All model providers failed:\n" + "\n".join(errors))

    def status(self) -> List[Dict[str, Any]]:
        now = time.time()
        return [
            {
                "name": p.name,
                "model": p.model,
                "available": self.cooldowns.get(p.name, 0) <= now,
                "cooldown_until": self.cooldowns.get(p.name, 0),
            }
            for p in self.providers
        ]
