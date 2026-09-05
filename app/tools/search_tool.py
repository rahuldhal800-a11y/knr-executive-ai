class SearchTool:
    def __init__(self):
        self._ddgs = None

    def _ensure_initialized(self):
        if self._ddgs is None:
            from duckduckgo_search import DDGS
            # Lazy initialize duckduckgo_search to avoid slow startup
            self._ddgs = DDGS()

    def get_tool_schemas(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Perform a web search using DuckDuckGo to get up-to-date information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to look up."
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "The maximum number of search results to return. Defaults to 5."
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]

    def web_search(self, query: str, max_results: int = 5) -> dict:
        self._ensure_initialized()
        try:
            results = list(self._ddgs.text(query, max_results=max_results))
            return {"ok": True, "results": results}
        except Exception as e:
            return {"ok": False, "message": f"Search failed: {str(e)}"}
