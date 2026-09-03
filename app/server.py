import os
from pathlib import Path
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Optional

# Configure standard logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("knr_brain_server")


from app.orchestrator import MultiAgentOrchestrator
from app.llm import LLMClient
from dotenv import load_dotenv

load_dotenv()


from fastapi.security.api_key import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    # Read the expected API key from the environment
    expected_api_key = os.getenv("APP_API_KEY")

    if not expected_api_key:
        # Fail closed: If no key is configured in the environment, deny access.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server configuration error: APP_API_KEY is not set."
        )

    if api_key_header == expected_api_key:
        return api_key_header

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
    )

app = FastAPI(title="KNR Integrity Central Brain Server")


import os
# Parse allowed origins from environment variable, default to local dev ports
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
async def chat_endpoint(request: ChatRequest, api_key: str = Depends(get_api_key)):
    try:
        logger.info(f"Processing chat request for provider: {request.provider}")
        # Initialize orchestrator
        orchestrator = MultiAgentOrchestrator(str(Path.cwd()))

        # Override the LLM client in the manager agent based on requested provider
        orchestrator.manager_agent.llm_client = LLMClient(provider=request.provider)

        # Process the request
        response_text = orchestrator.process_request(request.message)

        return JSONResponse(content={"ok": True, "response": response_text})
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)} ")
        return JSONResponse(content={"ok": False, "error": str(e)}, status_code=500)


# --- CRM Integration Endpoints ---

class LeadScoreRequest(BaseModel):
    budget_in_lakhs: float
    timeline_in_months: int
    property_type_interest: str = "Unknown"

@app.post("/api/v1/leads/score")
async def score_lead_endpoint(request: LeadScoreRequest, api_key: str = Depends(get_api_key)):
    """Direct API access to the SalesTool lead scoring logic for the CRM."""
    try:
        logger.info("Processing lead score request")
        # We can bypass the LLM and orchestrator for deterministic tool logic if needed,
        # or we could route it through the agent. For speed and reliability, calling the tool directly is best.
        from app.tools.sales_tool import SalesTool
        tool = SalesTool()
        result = tool.score_lead(
            budget_in_lakhs=request.budget_in_lakhs,
            timeline_in_months=request.timeline_in_months,
            property_type_interest=request.property_type_interest
        )
        if result["ok"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    except Exception as e:
        logger.error(f"Lead score endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

class DraftFollowUpRequest(BaseModel):
    client_name: str
    context: str
    urgency: str
    last_contact_date: str = "recently"
    provider: str = "openrouter" # Allow LLM provider selection for advanced drafting

@app.post("/api/v1/communications/draft")
async def draft_follow_up_endpoint(request: DraftFollowUpRequest, api_key: str = Depends(get_api_key)):
    """Generates a context-aware follow up email. Currently uses the deterministic tool, but easily upgradeable to use LLM."""
    try:
        logger.info(f"Processing draft follow up request for: {request.client_name}")
        from app.tools.sales_tool import SalesTool
        tool = SalesTool()
        result = tool.draft_follow_up(
            client_name=request.client_name,
            context=request.context,
            urgency=request.urgency,
            last_contact_date=request.last_contact_date
        )

        # Alternatively, we could route this through the agent for a more dynamic LLM generation:
        # orchestrator = MultiAgentOrchestrator(str(Path.cwd()))
        # orchestrator.manager_agent.llm_client = LLMClient(provider=request.provider)
        # prompt = f"Draft an email for {request.client_name}. Context: {request.context}. Urgency: {request.urgency}."
        # result = {"ok": True, "draft": orchestrator.process_request(prompt)}

        if result["ok"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    except Exception as e:
        logger.error(f"Draft follow up endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

class AgentTaskRequest(BaseModel):
    task_description: str
    provider: str = "openrouter"

@app.post("/api/v1/agent/task")
async def agent_task_endpoint(request: AgentTaskRequest, api_key: str = Depends(get_api_key)):
    """Run a full, autonomous multi-agent task triggered by the CRM."""
    try:
        logger.info("Processing agent task request")
        orchestrator = MultiAgentOrchestrator(str(Path.cwd()))
        orchestrator.manager_agent.llm_client = LLMClient(provider=request.provider)
        response_text = orchestrator.process_request(request.task_description)
        return {"ok": True, "result": response_text}
    except Exception as e:
        logger.error(f"Agent task endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- End CRM Integration Endpoints ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=True)
