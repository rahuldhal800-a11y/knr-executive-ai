import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.orchestrator import MultiAgentOrchestrator
from app.llm import LLMClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="KNR Integrity Central Brain Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

class ChatRequest(BaseModel):
    message: str
    provider: str = "openrouter"

@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = static_dir / "index.html"
    if index_path.exists():
        return index_path.read_text()
    return "<h1>Frontend not found. Please ensure app/static/index.html exists.</h1>"

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Initialize orchestrator
        orchestrator = MultiAgentOrchestrator(str(Path.cwd()))

        # Override the LLM client in the manager agent based on requested provider
        orchestrator.manager_agent.llm_client = LLMClient(provider=request.provider)

        # Process the request
        response_text = orchestrator.process_request(request.message)

        return JSONResponse(content={"ok": True, "response": response_text})
    except Exception as e:
        return JSONResponse(content={"ok": False, "error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=True)
