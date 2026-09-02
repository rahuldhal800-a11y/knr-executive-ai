import sys
import io
import contextlib

class CodeTool:
    def __init__(self):
        pass

    def get_tool_schemas(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "execute_code",
                    "description": "Execute Python code dynamically. Useful for data analysis, complex math, or running scripts. Note: code is executed in the current environment.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The Python code to execute."
                            }
                        },
                        "required": ["code"]
                    }
                }
            }
        ]

    def execute_code(self, code: str) -> dict:
        # Create a string buffer to capture stdout
        stdout_capture = io.StringIO()

        try:
            # Execute the code and capture any print statements
            with contextlib.redirect_stdout(stdout_capture):
                # We use exec to allow multi-line statements.
                # In a real production system, this should be sandboxed heavily.
                exec(code, globals())

            output = stdout_capture.getvalue()
            return {"ok": True, "output": output if output else "Code executed successfully with no output."}
        except Exception as e:
            return {"ok": False, "message": f"Execution failed: {str(e)}"}
