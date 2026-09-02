import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from dotenv import load_dotenv

load_dotenv()

console = Console()

BANNER = """
====================================
🤖 KNR Executive AI v0.3
  (Multi-Agent Autonomous Mode)
====================================
"""

HELP_TEXT = """
Welcome to the interactive multi-agent terminal.

You can speak in natural language to the AI.
It has powers to:
 - Access and manipulate the filesystem (read/write/create/delete).
 - Perform live web searches.
 - Save to and query long-term memory (RAG).

Type your request below.
Type 'clear' to clear the terminal.
Type 'exit' or 'quit' to close.
"""

def print_banner():
    console.print(Panel.fit(Text(BANNER, style="blue"), border_style="blue"))

def print_help():
    console.print(Panel(HELP_TEXT, title="Help", border_style="blue"))

def print_info(msg: str):
    console.print(f"[blue]{msg}[/blue]")

def print_error(msg: str):
    console.print(f"[red]{msg}[/red]")

def main_loop():
    # Setup OpenAI key check
    if not os.getenv("OPENAI_API_KEY"):
        print_error("Error: OPENAI_API_KEY not found in environment or .env file.")
        print_info("Please set it before using the AI.")
        return

    print_banner()
    print_help()

    orchestrator = None

    while True:
        try:
            raw = console.input("[bold green]You > [/bold green]")
        except (KeyboardInterrupt, EOFError):
            console.print()
            print_info("Exiting.")
            break

        if not raw.strip():
            continue

        cmd = raw.lower().strip()

        if cmd == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue
        elif cmd in ["exit", "quit"]:
            print_info("Goodbye.")
            break

        try:
            with console.status("[bold yellow]AI is thinking (and possibly using tools)...[/bold yellow]", spinner="dots"):
                if orchestrator is None:
                    # Lazy load heavy dependencies to improve startup time
                    from app.orchestrator import MultiAgentOrchestrator
                    orchestrator = MultiAgentOrchestrator(str(Path.cwd()))

                response = orchestrator.process_request(raw)

            console.print(Panel(Markdown(response), title="AI", border_style="green"))

        except Exception as e:
            print_error(f"An error occurred: {e}")

def main():
    main_loop()

if __name__ == "__main__":
    main()
