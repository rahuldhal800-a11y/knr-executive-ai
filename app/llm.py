import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self._client = None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @property
    def client(self):
        # ⚡ Bolt Optimization: Lazy load the OpenAI client to speed up initial CLI startup.
        # This reduces module import time and overall app startup time.
        if self._client is None:
            from openai import OpenAI
            # Initialize the OpenAI client
            # It will automatically use the OPENAI_API_KEY environment variable if it's set
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
