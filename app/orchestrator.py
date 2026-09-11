from pathlib import Path
from app.llm import LLMClient
from app.agent import Agent
from app.tools.file_tool import FileTool
from app.tools.search_tool import SearchTool
from app.tools.memory_tool import MemoryTool


class CompositeToolHandler:
    def __init__(self, tools_list):
        self.tools = tools_list

    def __getattr__(self, name):
        for tool in self.tools:
            if hasattr(tool, name):
                return getattr(tool, name)
        raise AttributeError(f"No tool has method '{name}'")


class MultiAgentOrchestrator:
    def __init__(self, base_path: str = "."):
        self.llm_client = LLMClient()
        root = Path(base_path).resolve()
        self.file_tool = FileTool(root)
        self.search_tool = SearchTool()
        self.memory_tool = MemoryTool(db_path=str(root / ".chroma_db"))
        self.manager_tools = (
            self.file_tool.get_tool_schemas()
            + self.search_tool.get_tool_schemas()
            + self.memory_tool.get_tool_schemas()
        )
        self.manager_tool_handler = CompositeToolHandler(
            [self.file_tool, self.search_tool, self.memory_tool]
        )
        prompt = """You are the KNR Executive AI autonomous work manager.

Turn the user's goal into concrete actions. Use available tools instead of merely describing what to do. Break large work into verifiable steps, inspect existing files before changing them, preserve user data, and report what was actually completed. Use web search for current information and memory only for durable project context. Never claim an action succeeded unless a tool result confirms it.

You are a general digital-work agent: research, document work, content production, project operations, codebase maintenance, data preparation, and business workflows. Ask only when an essential external decision or credential is genuinely unavailable; otherwise make reasonable reversible choices and execute.
"""
        self.manager_agent = Agent(
            name="ExecutiveManager",
            llm_client=self.llm_client,
            system_prompt=prompt,
            tools=self.manager_tools,
            tool_handler=self.manager_tool_handler,
            max_steps=int(__import__('os').getenv("AGENT_MAX_STEPS", "24")),
        )

    def process_request(self, user_input: str) -> str:
        self.manager_agent.add_user_message(user_input)
        return self.manager_agent.run()

    def model_status(self):
        return self.llm_client.status()
