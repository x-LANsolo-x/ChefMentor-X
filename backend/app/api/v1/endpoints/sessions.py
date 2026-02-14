"""
Cooking Session API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.core.dependencies import get_current_user
from app.db.base import get_db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.session import CookingSession, FailureAnalysis
from app.schemas.session import (
    CookingSessionCreate,
    CookingSessionUpdate,
    CookingSessionResponse,
    SessionStepUpdate,
    FailureAnalysisCreate,
    FailureAnalysisResponse
)

router = APIRouter()


@router.post("/", response_model=CookingSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_cooking_session(
    session_data: CookingSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Start a new cooking session.
    
    Args:
        session_data: Session creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        CookingSessionResponse: Created cooking session
    """
    # Verify recipe exists
    recipe_result = await db.execute(
        select(Recipe).where(Recipe.id == session_data.recipe_id)
    )
    recipe = recipe_result.scalar_one_or_none()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Create session
    cooking_session = CookingSession(
        user_id=current_user.id,
        recipe_id=session_data.recipe_id,
        session_type=session_data.session_type,
        status="in_progress",
        current_step=1,
        started_at=datetime.utcnow(),
        session_data={}
    )
    
    db.add(cooking_session)
    await db.commit()
    await db.refresh(cooking_session)
    
    return cooking_session


@router.get("/", response_model=List[CookingSessionResponse])
async def list_user_sessions(
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List cooking sessions for current user.
    
    Args:
        status_filter: Optional status filter
        limit: Maximum number of sessions to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List[CookingSessionResponse]: List of cooking sessions
    """
    stmt = select(CookingSession).where(CookingSession.user_id == current_user.id)
    
    if status_filter:
        stmt = stmt.where(CookingSession.status == status_filter)
    
    stmt = stmt.order_by(CookingSession.started_at.desc()).limit(limit)
    
    result = await db.execute(stmt)
    sessions = result.scalars().all()
    
    return sessions


@router.get("/{session_id}", response_model=CookingSessionResponse)
async def get_cooking_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific cooking session.
    
    Args:
        session_id: Session UUID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        CookingSessionResponse: Cooking session details
    """
    result = await db.execute(
        select(CookingSession).where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session


@router.put("/{session_id}", response_model=CookingSessionResponse)
async def update_cooking_session(
    session_id: UUID,
    session_update: CookingSessionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a cooking session (status, step, data).
    
    Args:
        session_id: Session UUID
        session_update: Session update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        CookingSessionResponse: Updated cooking session
    """
    result = await db.execute(
        select(CookingSession).where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Update fields
    update_data = session_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "session_data" and value:
            # Merge session data
            session.session_data = {**session.session_data, **value}
        else:
            setattr(session, field, value)
    
    # If status is completed, set completed_at
    if session_update.status == "completed":
        session.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(session)
    
    return session


@router.post("/{session_id}/step", response_model=CookingSessionResponse)
async def update_session_step(
    session_id: UUID,
    step_update: SessionStepUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current step in a cooking session.
    
    Args:
        session_id: Session UUID
        step_update: Step update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        CookingSessionResponse: Updated cooking session
    """
    result = await db.execute(
        select(CookingSession).where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Update current step
    session.current_step = step_update.step_number
    
    # Store step completion in session_data
    session_data = session.session_data or {}
    if "completed_steps" not in session_data:
        session_data["completed_steps"] = []
    
    if step_update.completed and step_update.step_number not in session_data["completed_steps"]:
        session_data["completed_steps"].append(step_update.step_number)
    
    if step_update.notes:
        if "step_notes" not in session_data:
            session_data["step_notes"] = {}
        session_data["step_notes"][str(step_update.step_number)] = step_update.notes
    
    session.session_data = session_data
    
    await db.commit()
    await db.refresh(session)
    
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cooking_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a cooking session.
    
    Args:
        session_id: Session UUID
        current_user: Current authenticated user
        db: Database session
    """
    result = await db.execute(
        select(CookingSession).where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    await db.delete(session)
    await db.commit()
    
    return None
