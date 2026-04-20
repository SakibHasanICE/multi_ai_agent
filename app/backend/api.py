from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.components.ai_agent import get_response_from_ai_agents
import traceback
import logging
import sys

from app.config.settings import settings

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

# Force logs to stdout so ECS/CloudWatch captures them
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = get_logger(__name__)

app = FastAPI(title="Multi AI Agent")

class RequestState(BaseModel):
    model_config = {"protected_namespaces": ()}  # Fix pydantic warning
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "groq_key_set": bool(settings.GROQ_API_KEY),
        "tavily_key_set": bool(settings.TAVILY_API_KEY),
        "allowed_models": settings.ALLOWED_MODEL_NAMES
    }


@app.post("/chat")
def chat_endpoint(request: RequestState):
    logger.info(f"Received request for model: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning(f"Invalid model name: {request.model_name}")
        raise HTTPException(status_code=400, detail=f"Invalid model name: {request.model_name}. Allowed: {settings.ALLOWED_MODEL_NAMES}")

    try:
        response = get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )
        logger.info(f"Successfully got response from AI Agent: {request.model_name}")
        return {"response": response}

    except Exception as e:
        error_trace = traceback.format_exc()
        # Print to stdout - this WILL appear in ECS logs
        print("=" * 60, flush=True)
        print("FULL ERROR TRACEBACK:", flush=True)
        print(error_trace, flush=True)
        print("=" * 60, flush=True)
        logger.error(f"Error during response generation: {str(e)}")
        logger.error(f"Traceback: {error_trace}")
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)} | Trace: {error_trace}"
        )