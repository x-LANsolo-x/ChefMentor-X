"""
Demo Session API endpoints for guest users.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import secrets

from app.db.base import get_db
from app.models.session import DemoSession
from app.schemas.user import DemoSessionCreate, DemoSessionResponse

router = APIRouter()


@router.post("/start", response_model=DemoSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_demo_session(
    demo_request: DemoSessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Start a new demo session for guest users.
    
    Args:
        demo_request: Demo session creation data with device_id
        db: Database session
        
    Returns:
        DemoSessionResponse: Created demo session with token
    """
    # Check if active session exists for this device
    result = await db.execute(
        select(DemoSession).where(
            DemoSession.device_id == demo_request.device_id,
            DemoSession.is_active == True,
            DemoSession.expires_at > datetime.utcnow()
        )
    )
    existing_session = result.scalar_one_or_none()
    
    if existing_session:
        return existing_session
    
    # Create new demo session
    session_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=7)  # 7-day expiry
    
    demo_session = DemoSession(
        device_id=demo_request.device_id,
        session_token=session_token,
        is_active=True,
        expires_at=expires_at
    )
    
    db.add(demo_session)
    await db.commit()
    await db.refresh(demo_session)
    
    return demo_session


@router.post("/end/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def end_demo_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    End a demo session.
    
    Args:
        session_id: Demo session ID
        db: Database session
    """
    result = await db.execute(
        select(DemoSession).where(DemoSession.id == session_id)
    )
    demo_session = result.scalar_one_or_none()
    
    if not demo_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demo session not found"
        )
    
    demo_session.is_active = False
    await db.commit()
    
    return None


@router.get("/validate/{session_token}", response_model=DemoSessionResponse)
async def validate_demo_session(
    session_token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Validate a demo session token.
    
    Args:
        session_token: Session token to validate
        db: Database session
        
    Returns:
        DemoSessionResponse: Demo session if valid
        
    Raises:
        HTTPException: If session is invalid or expired
    """
    result = await db.execute(
        select(DemoSession).where(
            DemoSession.session_token == session_token,
            DemoSession.is_active == True
        )
    )
    demo_session = result.scalar_one_or_none()
    
    if not demo_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demo session not found or inactive"
        )
    
    if demo_session.expires_at < datetime.utcnow():
        demo_session.is_active = False
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Demo session expired"
        )
    
    return demo_session
