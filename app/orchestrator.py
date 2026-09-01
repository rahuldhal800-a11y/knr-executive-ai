from pathlib import Path
from app.llm import LLMClient
from app.agent import Agent
from app.tools.file_tool import FileTool
from app.tools.search_tool import SearchTool
from app.tools.memory_tool import MemoryTool

class CompositeToolHandler:
    """A helper class to delegate tool calls to multiple tool instances."""
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

        # Initialize tools
        self.file_tool = FileTool(Path(base_path))
        self.search_tool = SearchTool()
        self.memory_tool = MemoryTool(db_path=str(Path(base_path) / ".chroma_db"))

        # Combine all tools for the manager
        self.manager_tools = self.file_tool.get_tool_schemas() + self.search_tool.get_tool_schemas() + self.memory_tool.get_tool_schemas()
        self.manager_tool_handler = CompositeToolHandler([self.file_tool, self.search_tool, self.memory_tool])

        # Define File System Agent
        fs_system_prompt = (
            "You are a File System Agent. You are specialized in reading, writing, and manipulating files and directories. "
            "You have access to a suite of file tools. Use them to fulfill the user's request. "
            "Always be careful not to delete important files. "
            "Return a clear summary of the actions you took and the result."
        )
        self.fs_agent = Agent(
            name="FileSystemAgent",
            llm_client=self.llm_client,
            system_prompt=fs_system_prompt,
            tools=self.file_tool.get_tool_schemas(),
            tool_handler=self.file_tool
        )

        # Define Manager Agent
        manager_system_prompt = (
            "You are the Manager Agent for KNR Executive AI. "
            "Your job is to understand the user's high-level goal and solve it. "
            "You have direct access to file system operations, web search, and a long-term memory store through your tools. "
            "Analyze the problem, use your tools (like web_search for current info, save_memory to learn/remember, or file tools) to accomplish the task, and provide a clear and concise final answer to the user."
        )
        self.manager_agent = Agent(
            name="ManagerAgent",
            llm_client=self.llm_client,
            system_prompt=manager_system_prompt,
            tools=self.manager_tools,
            tool_handler=self.manager_tool_handler
        )

    def process_request(self, user_input: str) -> str:
        """Process a user request through the multi-agent system."""
        # For this version, the manager agent directly handles the tools and executes the task
        self.manager_agent.add_user_message(user_input)
        return self.manager_agent.run()
