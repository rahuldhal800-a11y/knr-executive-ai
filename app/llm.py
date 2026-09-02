import os
from openai import OpenAI
from dotenv import load_dotenv

class LLMClient:
    def __init__(self, provider: str = "openrouter"):
        load_dotenv(override=True)
        self.provider = provider.lower()
        self.client = self._initialize_client()

    def _initialize_client(self):
        # OpenRouter (Default)
        if self.provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
            self.model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct")
            return OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )

        # Groq
        elif self.provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
            return OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )

        # Mistral
        elif self.provider == "mistral":
            api_key = os.getenv("MISTRAL_API_KEY")
            self.model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")
            return OpenAI(
                base_url="https://api.mistral.ai/v1",
                api_key=api_key
            )

        # DeepSeek
        elif self.provider == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY")
            self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            return OpenAI(
                base_url="https://api.deepseek.com/v1",
                api_key=api_key
            )

        # OpenAI (Standard fallback)
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            return OpenAI(api_key=api_key)

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
