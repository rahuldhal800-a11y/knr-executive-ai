import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        # We will lazy-initialize the client to avoid importing openai on startup
        self.client = None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def _get_client(self):
        if self.client is None:
            # Lazy import to improve startup time
            from openai import OpenAI
            # It will automatically use the OPENAI_API_KEY environment variable if it's set
            self.client = OpenAI()
        return self.client

    def chat_completion(self, messages, tools=None, tool_choice="auto"):
        kwargs = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice

        client = self._get_client()
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message
