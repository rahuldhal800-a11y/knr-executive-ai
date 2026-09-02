from pathlib import Path
from app.llm import LLMClient
from app.agent import Agent
from app.tools.file_tool import FileTool
from app.tools.search_tool import SearchTool
from app.tools.memory_tool import MemoryTool
from app.tools.sales_tool import SalesTool
from app.tools.code_tool import CodeTool
from app.tools.scrape_tool import ScrapeTool

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
        self.sales_tool = SalesTool()
        self.code_tool = CodeTool()
        self.scrape_tool = ScrapeTool()

        # Combine all tools for the manager
        self.manager_tools = (
            self.file_tool.get_tool_schemas() +
            self.search_tool.get_tool_schemas() +
            self.memory_tool.get_tool_schemas() +
            self.sales_tool.get_tool_schemas() +
            self.code_tool.get_tool_schemas() +
            self.scrape_tool.get_tool_schemas()
        )
        self.manager_tool_handler = CompositeToolHandler([
            self.file_tool,
            self.search_tool,
            self.memory_tool,
            self.sales_tool,
            self.code_tool,
            self.scrape_tool
        ])

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
            "You are the KNR Integrity Central Brain, a highly advanced, multi-agent AI automation capacity system. "
            "You are NOT a normal AI; you are the core intelligence driving real estate sales and operations for KNR. "
            "Your job is to understand high-level goals, qualify and score leads, draft communications, perform web research, "
            "scrape websites, execute dynamic Python code, and manage files and memories autonomously. "
            "You have direct access to file system operations, web search, scraping, code execution, long-term memory store, and specialized sales tools. "
            "Analyze problems, proactively use your tools (like execute_code, scrape_url, score_lead, draft_follow_up, web_search, save_memory) to accomplish tasks, "
            "and provide clear, strategic, and concise final answers to the user. Always think like the most advanced real estate brain."
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
