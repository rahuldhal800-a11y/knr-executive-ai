import os
from pathlib import Path
import shutil
from typing import Union, Dict, Any


class FileTool:
    """A production-quality filesystem tool using pathlib and shutil.

    Methods return dictionaries with:
      - ok: bool
      - message: str
      - content/items (optional)

    All paths are resolved against a base directory to avoid accidental escapes.
    """

    def __init__(self, base_path: Union[str, Path] = "."):
        self.base = Path(base_path).resolve()

    def get_tool_schemas(self):
        """Returns JSON schemas for OpenAI function calling."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "List files and folders in the given path (relative to the base directory).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The directory path to list files from. Defaults to the current directory."
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_folder",
                    "description": "Create a folder and any missing parents.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The path of the folder to create."
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_file",
                    "description": "Create an empty file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The path of the file to create."
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Display contents of a file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The path of the file to read."
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Overwrite a file with text. If the file or parents do not exist, they will be created.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The path of the file to write to."
                            },
                            "content": {
                                "type": "string",
                                "description": "The text content to write into the file."
                            }
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "append_file",
                    "description": "Append text to a file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The path of the file to append to."
                            },
                            "content": {
                                "type": "string",
                                "description": "The text content to append into the file."
                            }
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "rename",
                    "description": "Rename a file or folder inside the working directory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "old_path": {
                                "type": "string",
                                "description": "The current path of the file or folder."
                            },
                            "new_path": {
                                "type": "string",
                                "description": "The new path for the file or folder."
                            }
                        },
                        "required": ["old_path", "new_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "move",
                    "description": "Move a file or folder.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "old_path": {
                                "type": "string",
                                "description": "The current path of the file or folder."
                            },
                            "new_path": {
                                "type": "string",
                                "description": "The destination path for the file or folder."
                            }
                        },
                        "required": ["old_path", "new_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "copy",
                    "description": "Copy a file or folder. Copying directories requires the destination to not already exist.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "source": {
                                "type": "string",
                                "description": "The path of the file or folder to copy."
                            },
                            "destination": {
                                "type": "string",
                                "description": "The destination path to copy to."
                            }
                        },
                        "required": ["source", "destination"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete",
                    "description": "Delete a file or folder (recursively for folders).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The path of the file or folder to delete."
                            }
                        },
                        "required": ["path"]
                    }
                }
            }
        ]

    def _resolve(self, path: Union[str, Path]) -> Path:
        p = (self.base / Path(path)).resolve()
        try:
            # Ensure resolved path is inside base to avoid path escaping
            if str(p) == str(self.base) or str(p).startswith(str(self.base) + str(Path("/"))):
                return p
            else:
                raise ValueError("Path is outside the working directory")
        except Exception:
            # Re-raise as ValueError for callers
            raise ValueError("Path is outside the working directory")

    def list_files(self, path: Union[str, Path] = ".") -> Dict[str, Any]:
        try:
            p = self._resolve(path)
            if not p.exists():
                return {"ok": False, "message": f"Path does not exist: {p}"}
            if not p.is_dir():
                return {"ok": False, "message": f"Not a directory: {p}"}

            items = []
            # ⚡ Bolt Optimization: Use os.scandir instead of Path.iterdir()
            # os.scandir is much faster for listing files as it retrieves file type
            # and size info from the directory entry, reducing the number of stat() syscalls.
            with os.scandir(p) as it:
                entries = sorted(it, key=lambda e: e.name)
                for entry in entries:
                    is_dir = entry.is_dir()
                    kind = "[D]" if is_dir else "[F]"
                    try:
                        size = entry.stat().st_size if not is_dir else 0
                    except Exception:
                        size = 0

                    rel_path = str(Path(entry.path).relative_to(self.base))
                    items.append({"name": entry.name, "path": rel_path, "kind": kind, "size": size})

            return {"ok": True, "message": f"Listed {len(items)} items in {p}", "items": items}
        except ValueError as e:
            return {"ok": False, "message": str(e)}
        except Exception as e:
            return {"ok": False, "message": f"Unexpected error listing files: {e}"}

    def create_folder(self, path: Union[str, Path]) -> Dict[str, Any]:
        try:
            p = self._resolve(path)
            p.mkdir(parents=True, exist_ok=True)
            return {"ok": True, "message": f"Folder created: {p.relative_to(self.base)}"}
        except ValueError as e:
            return {"ok": False, "message": str(e)}
        except Exception as e:
            return {"ok": False, "message": f"Failed to create folder: {e}"}

    def create_file(self, path: Union[str, Path]) -> Dict[str, Any]:
        try:
            p = self._resolve(path)
            if p.exists():
                return {"ok": False, "message": f"File already exists: {p.relative_to(self.base)}"}
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("")
            return {"ok": True, "message": f"File created: {p.relative_to(self.base)}"}
        except ValueError as e:
            return {"ok": False, "message": str(e)}
        except Exception as e:
            return {"ok": False, "message": f"Failed to create file: {e}"}

    def read_file(self, path: Union[str, Path]) -> Dict[str, Any]:
        try:
            p = self._resolve(path)
            if not p.exists():
                return {"ok": False, "message": f"File does not exist: {p.relative_to(self.base)}"}
            if not p.is_file():
                return {"ok": False, "message": f"Not a file: {p.relative_to(self.base)}"}
            content = p.read_text()
            return {"ok": True, "message": f"Read file: {p.relative_to(self.base)}", "content": content}
        except ValueError as e:
            return {"ok": False, "message": str(e)}
        except Exception as e:
            return {"ok": False, "message": f"Failed to read file: {e}"}

    def write_file(self, path: Union[str, Path], content: str) -> Dict[str, Any]:
        try:
            p = self._resolve(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
            return {"ok": True, "message": f"Wrote to file: {p.relative_to(self.base)}"}
        except ValueError as e:
            return {"ok": False, "message": str(e)}
        except Exception as e:
            return {"ok": False, "message": f"Failed to write file: {e}"}

    def append_file(self, path: Union[str, Path], content: str) -> Dict[str, Any]:
        try:
            p = self._resolve(path)
            if not p.exists():
                # create file if missing
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content)
                return {"ok": True, "message": f"File created and content appended: {p.relative_to(self.base)}"}
            if not p.is_file():
                return {"ok": False, "message": f"Not a file: {p.relative_to(self.base)}"}
            with p.open("a", encoding="utf-8") as f:
                f.write(content)
            return {"ok": True, "message": f"Appended to file: {p.relative_to(self.base)}"}
        except ValueError as e:
            return {"ok": False, "message": str(e)}
        except Exception as e:
            return {"ok": False, "message": f"Failed to append to file: {e}"}

    def rename(self, old_path: Union[str, Path], new_path: Union[str, Path]) -> Dict[str, Any]:
        try:
            old = self._resolve(old_path)
            new = self._resolve(new_path)
            if not old.exists():
                return {"ok": False, "message": f"Source does not exist: {old.relative_to(self.base)}"}
            new.parent.mkdir(parents=True, exist_ok=True)
            old.rename(new)
            return {"ok": True, "message": f"Renamed {old.relative_to(self.base)} -> {new.relative_to(self.base)}"}
        except ValueError as e:
            return {"ok": False, "message": str(e)}
        except Exception as e:
            return {"ok": False, "message": f"Failed to rename: {e}"}

    def move(self, old_path: Union[str, Path], new_path: Union[str, Path]) -> Dict[str, Any]:
        try:
            old = self._resolve(old_path)
            new = self._resolve(new_path)
            if not old.exists():
                return {"ok": False, "message": f"Source does not exist: {old.relative_to(self.base)}"}
            new_parent = new.parent
            new_parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old), str(new))
            return {"ok": True, "message": f"Moved {old.relative_to(self.base)} -> {new.relative_to(self.base)}"}
        except ValueError as e:
            return {"ok": False, "message": str(e)}
        except Exception as e:
            return {"ok": False, "message": f"Failed to move: {e}"}

    def copy(self, source: Union[str, Path], destination: Union[str, Path]) -> Dict[str, Any]:
        try:
            src = self._resolve(source)
            dst = self._resolve(destination)
            if not src.exists():
                return {"ok": False, "message": f"Source does not exist: {src.relative_to(self.base)}"}
            dst_parent = dst.parent
            dst_parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                # copytree requires destination to not exist
                if dst.exists():
                    return {"ok": False, "message": f"Destination already exists: {dst.relative_to(self.base)}"}
                shutil.copytree(str(src), str(dst))
            else:
                shutil.copy2(str(src), str(dst))
            return {"ok": True, "message": f"Copied {src.relative_to(self.base)} -> {dst.relative_to(self.base)}"}
        except ValueError as e:
            return {"ok": False, "message": str(e)}
        except Exception as e:
            return {"ok": False, "message": f"Failed to copy: {e}"}

    def delete(self, path: Union[str, Path]) -> Dict[str, Any]:
        try:
            p = self._resolve(path)
            if not p.exists():
                return {"ok": False, "message": f"Path does not exist: {p.relative_to(self.base)}"}
            if p.is_dir():
                shutil.rmtree(str(p))
            else:
                p.unlink()
            return {"ok": True, "message": f"Deleted: {p.relative_to(self.base)}"}
        except ValueError as e:
            return {"ok": False, "message": str(e)}
        except Exception as e:
            return {"ok": False, "message": f"Failed to delete: {e}"}
