import json
from typing import List, Dict, Any, Optional


class Agent:
    def __init__(self, name: str, llm_client: Any, system_prompt: str, tools: Optional[List[Dict[str, Any]]] = None, tool_handler: Optional[Any] = None, max_steps: int = 24):
        self.name = name
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.tools = tools
        self.tool_handler = tool_handler
        self.max_steps = max_steps
        self.messages: List[Dict[str, Any]] = [{"role": "system", "content": self.system_prompt}]

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def run(self) -> str:
        """Run an agent with bounded tool loops and provider failover."""
        for _ in range(self.max_steps):
            response_msg = self.llm_client.chat_completion(self.messages, tools=self.tools)
            self.messages.append(response_msg.model_dump(exclude_none=True))
            if not response_msg.tool_calls:
                return response_msg.content or "Task completed without a textual response."

            for tool_call in response_msg.tool_calls:
                func_name = tool_call.function.name
                try:
                    func_args = json.loads(tool_call.function.arguments or "{}")
                    if hasattr(self.tool_handler, func_name):
                        result = getattr(self.tool_handler, func_name)(**func_args)
                    else:
                        result = {"ok": False, "message": f"Tool '{func_name}' is not available."}
                except Exception as exc:
                    result = {"ok": False, "message": f"Tool '{func_name}' failed: {exc}"}
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": json.dumps(result, default=str),
                })
        return f"Stopped after {self.max_steps} agent steps. Continue the task with another request if needed."
