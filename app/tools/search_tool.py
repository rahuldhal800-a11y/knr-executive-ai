class SearchTool:
    def __init__(self):
        # Initialize lazily to improve startup performance
        self._ddgs = None

    @property
    def ddgs(self):
        if self._ddgs is None:
            from duckduckgo_search import DDGS
            self._ddgs = DDGS()
        return self._ddgs

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
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            return {"ok": True, "results": results}
        except Exception as e:
            return {"ok": False, "message": f"Search failed: {str(e)}"}
