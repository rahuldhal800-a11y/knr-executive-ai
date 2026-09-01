import json
from typing import List, Dict, Any, Optional

class Agent:
    def __init__(self, name: str, llm_client: Any, system_prompt: str, tools: Optional[List[Dict[str, Any]]] = None, tool_handler: Optional[Any] = None):
        self.name = name
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.tools = tools
        self.tool_handler = tool_handler
        self.messages: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt}
        ]

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def run(self) -> str:
        """Run the agent until it provides a final response, handling tool calls if necessary."""
        while True:
            response_msg = self.llm_client.chat_completion(self.messages, tools=self.tools)

            # Add the assistant's message to history
            # the dict structure is needed as `response_msg` is a Pydantic object
            self.messages.append(response_msg.model_dump(exclude_none=True))

            # If no tool calls, this is the final answer
            if not response_msg.tool_calls:
                return response_msg.content

            # Handle tool calls
            for tool_call in response_msg.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                print(f"[Agent {self.name}] Executing tool '{func_name}' with args: {func_args}")

                try:
                    # Dynamically call the method on the tool handler
                    if hasattr(self.tool_handler, func_name):
                        func = getattr(self.tool_handler, func_name)
                        result = func(**func_args)
                    else:
                        result = {"ok": False, "message": f"Tool '{func_name}' not found on handler."}
                except Exception as e:
                    result = {"ok": False, "message": f"Error executing '{func_name}': {str(e)}"}

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": json.dumps(result)
                })
