import chromadb
import uuid

class MemoryTool:
    def __init__(self, db_path: str = "./.chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="ai_memory")

    def get_tool_schemas(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "save_memory",
                    "description": "Save important information to your long-term memory for future retrieval. Use this to remember facts, user preferences, or context.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The information to save to memory."
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Optional key-value pairs associated with the memory."
                            }
                        },
                        "required": ["content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_memory",
                    "description": "Search your long-term memory for information previously saved.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to look up in memory."
                            },
                            "n_results": {
                                "type": "integer",
                                "description": "The maximum number of memory items to return. Defaults to 3."
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]

    def save_memory(self, content: str, metadata: dict = None) -> dict:
        try:
            doc_id = str(uuid.uuid4())
            self.collection.add(
                documents=[content],
                metadatas=[metadata] if metadata else None,
                ids=[doc_id]
            )
            return {"ok": True, "message": "Memory saved successfully.", "id": doc_id}
        except Exception as e:
            return {"ok": False, "message": f"Failed to save memory: {str(e)}"}

    def search_memory(self, query: str, n_results: int = 3) -> dict:
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            # Formatting the response
            memories = []
            if results and results.get("documents") and len(results["documents"]) > 0:
                for i, doc in enumerate(results["documents"][0]):
                    memories.append({
                        "id": results["ids"][0][i],
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results.get("metadatas") else None
                    })

            return {"ok": True, "memories": memories}
        except Exception as e:
            return {"ok": False, "message": f"Failed to search memory: {str(e)}"}
