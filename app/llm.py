import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        # We will lazy initialize the OpenAI client to improve startup speed
        self._client = None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def _ensure_initialized(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI()

    def chat_completion(self, messages, tools=None, tool_choice="auto"):
        self._ensure_initialized()
        kwargs = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice

        response = self._client.chat.completions.create(**kwargs)
        return response.choices[0].message
