from typing import Any, Dict, List

from app.provider_router import ModelRouter


class LLMClient:
    """Backward-compatible facade around the multi-provider model router."""

    def __init__(self):
        self.router = ModelRouter()

    def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        tools=None,
        tool_choice="auto",
    ):
        return self.router.chat_completion(messages, tools=tools, tool_choice=tool_choice)

    def status(self):
        return self.router.status()
