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

@router.post("/{session_id}/next", response_model=StepResponse)
async def next_step(
    session_id: str, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """User says 'Next' -> Advance step and return new instruction"""
    service = CookingService(db)
    return await service.advance_step(session_id, background_tasks)
