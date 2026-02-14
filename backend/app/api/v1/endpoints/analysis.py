"""
Failure Analysis API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.core.dependencies import get_current_user
from app.db.base import get_db
from app.models.user import User
from app.models.session import CookingSession, FailureAnalysis
from app.schemas.session import (
    FailureAnalysisCreate,
    FailureAnalysisResponse
)

router = APIRouter()


@router.post("/", response_model=FailureAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_failure_analysis(
    analysis_data: FailureAnalysisCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a failure analysis for a cooking session.
    
    Args:
        analysis_data: Failure analysis creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        FailureAnalysisResponse: Created failure analysis
    """
    # Verify session exists and belongs to user
    session_result = await db.execute(
        select(CookingSession).where(
            CookingSession.id == analysis_data.session_id,
            CookingSession.user_id == current_user.id
        )
    )
    session = session_result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or does not belong to user"
        )
    
    # Create failure analysis
    failure_analysis = FailureAnalysis(
        session_id=analysis_data.session_id,
        user_id=current_user.id,
        issue_description=analysis_data.issue_description,
        dish_image_url=analysis_data.dish_image_url,
        ai_diagnosis=None,  # Will be populated by AI service
        suggestions=[]  # Will be populated by AI service
    )
    
    db.add(failure_analysis)
    await db.commit()
    await db.refresh(failure_analysis)
    
    # TODO: Call AI service to analyze the failure and update ai_diagnosis and suggestions
    # This would be done asynchronously in a background task in production
    
    return failure_analysis


@router.get("/", response_model=List[FailureAnalysisResponse])
async def list_user_analyses(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List failure analyses for current user.
    
    Args:
        limit: Maximum number of analyses to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List[FailureAnalysisResponse]: List of failure analyses
    """
    result = await db.execute(
        select(FailureAnalysis)
        .where(FailureAnalysis.user_id == current_user.id)
        .order_by(FailureAnalysis.created_at.desc())
        .limit(limit)
    )
    analyses = result.scalars().all()
    
    return analyses


@router.get("/{analysis_id}", response_model=FailureAnalysisResponse)
async def get_failure_analysis(
    analysis_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific failure analysis.
    
    Args:
        analysis_id: Analysis UUID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        FailureAnalysisResponse: Failure analysis details
    """
    result = await db.execute(
        select(FailureAnalysis).where(
            FailureAnalysis.id == analysis_id,
            FailureAnalysis.user_id == current_user.id
        )
    )
    analysis = result.scalar_one_or_none()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failure analysis not found"
        )
    
    return analysis


@router.get("/session/{session_id}", response_model=List[FailureAnalysisResponse])
async def get_session_analyses(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all failure analyses for a specific session.
    
    Args:
        session_id: Session UUID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List[FailureAnalysisResponse]: List of failure analyses for the session
    """
    # Verify session belongs to user
    session_result = await db.execute(
        select(CookingSession).where(
            CookingSession.id == session_id,
            CookingSession.user_id == current_user.id
        )
    )
    session = session_result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or does not belong to user"
        )
    
    # Get all analyses for this session
    result = await db.execute(
        select(FailureAnalysis)
        .where(FailureAnalysis.session_id == session_id)
        .order_by(FailureAnalysis.created_at.desc())
    )
    analyses = result.scalars().all()
    
    return analyses


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_failure_analysis(
    analysis_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a failure analysis.
    
    Args:
        analysis_id: Analysis UUID
        current_user: Current authenticated user
        db: Database session
    """
    result = await db.execute(
        select(FailureAnalysis).where(
            FailureAnalysis.id == analysis_id,
            FailureAnalysis.user_id == current_user.id
        )
    )
    analysis = result.scalar_one_or_none()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failure analysis not found"
        )
    
    await db.delete(analysis)
    await db.commit()
    
    return None
