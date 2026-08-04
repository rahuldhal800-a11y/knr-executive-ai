import shlex
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from app.tools.file_tool import FileTool

console = Console()

BANNER = """
====================================
🤖 KNR Executive AI v0.2
====================================
"""

HELP_TEXT = """
Available Commands

help
list
create folder <folder>
create file <file>
read <file>
write <file> <text>
append <file> <text>
rename <old> <new>
move <old> <new>
copy <old> <new>
delete <file>
clear
exit

Examples:
create folder Test
create file notes.txt
write notes.txt Hello Rahul
append notes.txt Welcome
read notes.txt
rename notes.txt note.txt
copy note.txt backup.txt
move backup.txt Backup/backup.txt
delete backup.txt
clear
exit
"""


def print_banner():
    console.print(Panel.fit(Text(BANNER, style="blue"), border_style="blue"))


def print_help():
    console.print(Panel(HELP_TEXT, title="Help", border_style="blue"))


def print_success(msg: str):
    console.print(f"[green]{msg}[/green]")


def print_error(msg: str):
    console.print(f"[red]{msg}[/red]")


def print_info(msg: str):
    console.print(f"[blue]{msg}[/blue]")


def cmd_list(tool: FileTool, args: list):
    path = args[0] if args else "."
    res = tool.list_files(path)
    if not res.get("ok"):
        print_error(res.get("message"))
        return
    items = res.get("items", [])
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Kind", width=6)
    table.add_column("Name")
    table.add_column("Size", justify="right")
    for it in items:
        table.add_row(it["kind"], it["path"], str(it["size"]))
    console.print(table)


def main_loop():
    tool = FileTool(Path.cwd())
    print_banner()
    print_help()

    while True:
        try:
            raw = console.input("[bold blue]> [/bold blue]")
        except (KeyboardInterrupt, EOFError):
            console.print()
            print_info("Exiting.")
            break

        if not raw.strip():
            continue

        try:
            parts = shlex.split(raw)
        except ValueError as e:
            print_error(f"Failed to parse command: {e}")
            continue

        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "help":
            print_help()

        elif cmd == "list":
            cmd_list(tool, args)

        elif cmd == "create":
            if len(args) >= 2 and args[0].lower() == "folder":
                path = args[1]
                res = tool.create_folder(path)
                (print_success if res.get("ok") else print_error)(res.get("message"))
            elif len(args) >= 2 and args[0].lower() == "file":
                path = args[1]
                res = tool.create_file(path)
                (print_success if res.get("ok") else print_error)(res.get("message"))
            else:
                print_error("Usage: create folder <folder> | create file <file>")

        elif cmd == "read":
            if not args:
                print_error("Usage: read <file>")
                continue
            res = tool.read_file(args[0])
            if res.get("ok"):
                console.print(Panel(res.get("content", ""), title=args[0], border_style="blue"))
            else:
                print_error(res.get("message"))

        elif cmd == "write":
            if len(args) < 2:
                print_error("Usage: write <file> <text>")
                continue
            path = args[0]
            content = "".join(args[1:]) if len(args) > 1 else ""
            # If user provided spaces they should quote the text; but join ensures no delimiting spaces lost
            res = tool.write_file(path, content)
            (print_success if res.get("ok") else print_error)(res.get("message"))

        elif cmd == "append":
            if len(args) < 2:
                print_error("Usage: append <file> <text>")
                continue
            path = args[0]
            content = "".join(args[1:])
            res = tool.append_file(path, content)
            (print_success if res.get("ok") else print_error)(res.get("message"))

        elif cmd == "rename":
            if len(args) != 2:
                print_error("Usage: rename <old> <new>")
                continue
            res = tool.rename(args[0], args[1])
            (print_success if res.get("ok") else print_error)(res.get("message"))

        elif cmd == "move":
            if len(args) != 2:
                print_error("Usage: move <old> <new>")
                continue
            res = tool.move(args[0], args[1])
            (print_success if res.get("ok") else print_error)(res.get("message"))

        elif cmd == "copy":
            if len(args) != 2:
                print_error("Usage: copy <old> <new>")
                continue
            res = tool.copy(args[0], args[1])
            (print_success if res.get("ok") else print_error)(res.get("message"))

        elif cmd == "delete":
            if len(args) != 1:
                print_error("Usage: delete <file_or_folder>")
                continue
            res = tool.delete(args[0])
            (print_success if res.get("ok") else print_error)(res.get("message"))

        elif cmd == "clear":
            os.system("cls" if os.name == "nt" else "clear")

        elif cmd == "exit" or cmd == "quit":
            print_info("Goodbye.")
            break

        else:
            print_error(f"Unknown command: {cmd}. Type 'help' to list commands.")


def main():
    main_loop()


if __name__ == "__main__":
    main()
