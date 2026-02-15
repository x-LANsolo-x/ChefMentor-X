from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.schemas.cooking import StartCookingRequest, CookingSessionResponse, StepResponse
from app.services.cooking import CookingService

router = APIRouter()

@router.post("/start", response_model=CookingSessionResponse)
async def start_cooking(
    data: StartCookingRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Start cooking a specific recipe"""
    service = CookingService(db)
    session = await service.start_session(data.recipe_id, demo_session_id=data.demo_session_id, background_tasks=background_tasks)
    return session

@router.get("/{session_id}/current", response_model=StepResponse)
async def get_current_step(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get the current step instruction"""
    service = CookingService(db)
    return await service.get_current_step(session_id)

    """User says 'Next' -> Advance step and return new instruction"""
    service = CookingService(db)
    return await service.advance_step(session_id, background_tasks)

# ── Chat Endpoint ───────────────────────────────────

from pydantic import BaseModel
from app.services.ai_mentor import AIMentorService

class ChatRequest(BaseModel):
    messages: list[dict] # [{"role": "user", "content": "..."}]
    context: dict        # {"recipe_name": "...", "current_step": 1, ...}

@router.post("/chat")
async def chat_with_mentor(request: ChatRequest):
    """Interactive chat with the AI Chef"""
    service = AIMentorService()
    response = await service.chat_with_mentor(request.messages, request.context)
    return {"response": response}
