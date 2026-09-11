import json
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from dotenv import load_dotenv

from app.orchestrator import MultiAgentOrchestrator

load_dotenv()
console = Console()

BANNER = """
========================================
🧠 KNR AEGIS AI v1.0
  Autonomous Executive Agent
========================================
"""
HELP_TEXT = """Natural-language autonomous digital-work agent.

Commands:
  help      Show this help
  models    Show configured model providers and availability
  clear     Clear terminal
  exit      Exit

The agent can research, manipulate project files, use memory, and execute
multi-step work through its configured tools. Model quota/rate-limit failures
automatically fall through to the next configured provider.
"""


def main_loop():
    orchestrator = MultiAgentOrchestrator(str(Path.cwd()))
    console.print(Panel.fit(Text(BANNER, style="blue"), border_style="blue"))
    console.print(Panel(HELP_TEXT, title="Help", border_style="blue"))

    while True:
        try:
            raw = console.input("[bold green]You > [/bold green]")
        except (KeyboardInterrupt, EOFError):
            console.print()
            break
        if not raw.strip():
            continue
        cmd = raw.lower().strip()
        if cmd == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue
        if cmd in {"exit", "quit"}:
            break
        if cmd == "help":
            console.print(Panel(HELP_TEXT, title="Help", border_style="blue"))
            continue
        if cmd == "models":
            console.print_json(json.dumps(orchestrator.model_status(), default=str))
            continue
        try:
            with console.status("[bold yellow]Agent executing...[/bold yellow]", spinner="dots"):
                response = orchestrator.process_request(raw)
            console.print(Panel(Markdown(response), title="AEGIS", border_style="green"))
        except Exception as exc:
            console.print(f"[red]Agent error:[/red] {exc}")


if __name__ == "__main__":
    main_loop()
