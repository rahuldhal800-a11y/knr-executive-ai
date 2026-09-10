from pathlib import Path
from app.llm import LLMClient
from app.agent import Agent
from app.tools.file_tool import FileTool
from app.tools.search_tool import SearchTool
from app.tools.memory_tool import MemoryTool
from app.tools.sales_tool import SalesTool
from app.tools.scrape_tool import ScrapeTool
from app.tools.calc_tool import CalcTool

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
        self.scrape_tool = ScrapeTool()
        self.calc_tool = CalcTool()

        # Combine all tools for the manager
        self.manager_tools = (
            self.file_tool.get_tool_schemas() +
            self.search_tool.get_tool_schemas() +
            self.memory_tool.get_tool_schemas() +
            self.sales_tool.get_tool_schemas() +
            self.scrape_tool.get_tool_schemas() +
            self.calc_tool.get_tool_schemas()
        )
        self.manager_tool_handler = CompositeToolHandler([
            self.file_tool,
            self.search_tool,
            self.memory_tool,
            self.sales_tool,
            self.scrape_tool,
            self.calc_tool
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
            "You are the KNR Integrity Central Brain, an elite, hyper-intelligent Senior Real Estate Strategist and AI Operator. "
            "You are NOT a normal chatbot; you are the core intelligence driving multi-million dollar real estate operations for KNR. "
            "Your directives: "
            "1. ALWAYS prioritize revenue generation, swift lead conversion, and 100% data integrity. "
            "2. Think systematically: Analyze problems, formulate a plan, use your tools proactively, and execute. "
            "3. You have direct access to web search, scraping, long-term memory (SOPs), specialized sales scoring, and financial calculators. "
            "4. Never hallucinate facts about properties. If you don't know, use `web_search` or `search_memory`. "
            "5. Communicate with extreme professionalism, urgency, and precision. "
            "6. When asked to evaluate a deal, consider ROI, EMI, client psychology, and market trends. "
            "Provide clear, strategic, and actionable final answers to the user. You are the ultimate closer."
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
