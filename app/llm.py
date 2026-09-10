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
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY is missing in your .env file.")
            self.model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct")
            return OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )

        # Groq
        elif self.provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY is missing in your .env file.")
            self.model = os.getenv("GROQ_MODEL", "llama3-8b-8192")
            return OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )

        # Mistral
        elif self.provider == "mistral":
            api_key = os.getenv("MISTRAL_API_KEY")
            if not api_key:
                raise ValueError("MISTRAL_API_KEY is missing in your .env file.")
            self.model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")
            return OpenAI(
                base_url="https://api.mistral.ai/v1",
                api_key=api_key
            )

        # DeepSeek
        elif self.provider == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError("DEEPSEEK_API_KEY is missing in your .env file.")
            self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            return OpenAI(
                base_url="https://api.deepseek.com/v1",
                api_key=api_key
            )

        # Perplexity
        elif self.provider == "perplexity":
            api_key = os.getenv("PERPLEXITY_API_KEY")
            if not api_key:
                raise ValueError("PERPLEXITY_API_KEY is missing in your .env file.")
            self.model = os.getenv("PERPLEXITY_MODEL", "llama-3.1-sonar-large-128k-chat")
            return OpenAI(
                base_url="https://api.perplexity.ai",
                api_key=api_key
            )

        # HuggingFace
        elif self.provider == "huggingface":
            api_key = os.getenv("HUGGINGFACE_API_KEY")
            if not api_key:
                raise ValueError("HUGGINGFACE_API_KEY is missing in your .env file.")
            self.model = os.getenv("HUGGINGFACE_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
            return OpenAI(
                base_url="https://api-inference.huggingface.co/v1/",
                api_key=api_key
            )


        # Omniroute
        elif self.provider == "omniroute":
            api_key = os.getenv("OMNIROUTE_API_KEY")
            if not api_key:
                raise ValueError("OMNIROUTE_API_KEY is missing in your .env file.")
            self.model = os.getenv("OMNIROUTE_MODEL", "omniroute-default")
            return OpenAI(
                base_url="https://api.omniroute.com/v1", # Placeholder URL
                api_key=api_key
            )

        # Agnes
        elif self.provider == "agnes":
            api_key = os.getenv("AGNES_API_KEY")
            if not api_key:
                raise ValueError("AGNES_API_KEY is missing in your .env file.")
            self.model = os.getenv("AGNES_MODEL", "agnes-default")
            return OpenAI(
                base_url="https://api.agnes.ai/v1", # Placeholder URL
                api_key=api_key
            )

        # Nano GPT
        elif self.provider == "nano_gpt":
            api_key = os.getenv("NANO_GPT_API_KEY")
            if not api_key:
                raise ValueError("NANO_GPT_API_KEY is missing in your .env file.")
            self.model = os.getenv("NANO_GPT_MODEL", "nano-default")
            return OpenAI(
                base_url="https://api.nanogpt.ai/v1", # Placeholder URL
                api_key=api_key
            )

        # Xiaomi MIMO
        elif self.provider == "xiaomi_mimo":
            api_key = os.getenv("XIAOMI_MIMO_API_KEY")
            if not api_key:
                raise ValueError("XIAOMI_MIMO_API_KEY is missing in your .env file.")
            self.model = os.getenv("XIAOMI_MIMO_MODEL", "mimo-default")
            return OpenAI(
                base_url="https://api.xiaomi.com/v1", # Placeholder URL
                api_key=api_key
            )

        # Context 7
        elif self.provider == "context7":
            api_key = os.getenv("CONTEXT7_API_KEY")
            if not api_key:
                raise ValueError("CONTEXT7_API_KEY is missing in your .env file.")
            self.model = os.getenv("CONTEXT7_MODEL", "context7-default")
            return OpenAI(
                base_url="https://api.context7.ai/v1", # Placeholder URL
                api_key=api_key
            )

        # Search API
        elif self.provider == "search_api":
            api_key = os.getenv("SEARCH_API_KEY")
            if not api_key:
                raise ValueError("SEARCH_API_KEY is missing in your .env file.")
            self.model = os.getenv("SEARCH_API_MODEL", "search-default")
            return OpenAI(
                base_url="https://api.searchapi.io/v1", # Placeholder URL
                api_key=api_key
            )

        # Aion Labs
        elif self.provider == "aion_labs":
            api_key = os.getenv("AION_LABS_API_KEY")
            if not api_key:
                raise ValueError("AION_LABS_API_KEY is missing in your .env file.")
            self.model = os.getenv("AION_LABS_MODEL", "aion-default")
            return OpenAI(
                base_url="https://api.aionlabs.com/v1", # Placeholder URL
                api_key=api_key
            )

        # Arcee
        elif self.provider == "arcee":
            api_key = os.getenv("ARCEE_API_KEY")
            if not api_key:
                raise ValueError("ARCEE_API_KEY is missing in your .env file.")
            self.model = os.getenv("ARCEE_MODEL", "arcee-default")
            return OpenAI(
                base_url="https://api.arcee.ai/v1", # Placeholder URL
                api_key=api_key
            )

        # DeepInfra
        elif self.provider == "deepinfra":
            api_key = os.getenv("DEEPINFRA_API_KEY")
            if not api_key:
                raise ValueError("DEEPINFRA_API_KEY is missing in your .env file.")
            self.model = os.getenv("DEEPINFRA_MODEL", "meta-llama/Llama-2-70b-chat-hf")
            return OpenAI(
                base_url="https://api.deepinfra.com/v1/openai",
                api_key=api_key
            )

        # Cloudflare Workers AI
        elif self.provider == "cloudflare":
            account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
            api_key = os.getenv("CLOUDFLARE_API_KEY")
            if not account_id or not api_key:
                raise ValueError("CLOUDFLARE_ACCOUNT_ID or CLOUDFLARE_API_KEY missing.")
            self.model = os.getenv("CLOUDFLARE_MODEL", "@cf/meta/llama-2-7b-chat-int8")
            return OpenAI(
                base_url=f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1",
                api_key=api_key
            )

        # Sarvam AI
        elif self.provider == "sarvam":
            api_key = os.getenv("SARVAM_API_KEY")
            if not api_key:
                raise ValueError("SARVAM_API_KEY is missing in your .env file.")
            self.model = os.getenv("SARVAM_MODEL", "sarvam-default")
            return OpenAI(
                base_url="https://api.sarvam.ai/v1", # Placeholder URL
                api_key=api_key
            )

        # Bedrock (via standard OpenAI compat if proxy is set up, else placeholder)
        elif self.provider == "bedrock":
            api_key = os.getenv("BEDROCK_API_KEY")
            if not api_key:
                raise ValueError("BEDROCK_API_KEY is missing in your .env file.")
            self.model = os.getenv("BEDROCK_MODEL", "anthropic.claude-v2")
            return OpenAI(
                base_url="https://api.bedrock-proxy.com/v1", # Placeholder proxy URL
                api_key=api_key
            )

        # OpenAI (Standard fallback)
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY is missing in your .env file.")
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
