import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        # We don't initialize the OpenAI client immediately to avoid startup bottleneck
        # It will be lazy-loaded in the client property
        self._client = None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @property
    def client(self):
        # ⚡ Bolt Optimization: Lazy-load heavy ML dependency to improve startup time
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI()
        return self._client

    def chat_completion(self, messages, tools=None, tool_choice="auto"):
        kwargs = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message
