"""
Cooking Session schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


class CookingSessionBase(BaseModel):
    """Base schema for cooking session."""
    recipe_id: UUID
    session_type: str = Field(..., description="live or practice")


class CookingSessionCreate(CookingSessionBase):
    """Schema for creating a cooking session."""
    pass


class CookingSessionUpdate(BaseModel):
    """Schema for updating a cooking session."""
    status: Optional[str] = Field(None, description="in_progress, paused, completed, failed")
    current_step: Optional[int] = Field(None, ge=1)
    session_data: Optional[Dict[str, Any]] = None


class CookingSessionResponse(CookingSessionBase):
    """Response schema for cooking session."""
    id: UUID
    user_id: UUID
    status: str
    current_step: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    session_data: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        from_attributes = True


class SessionStepUpdate(BaseModel):
    """Schema for updating session step progress."""
    step_number: int = Field(..., ge=1)
    completed: bool = False
    notes: Optional[str] = None


class FailureAnalysisBase(BaseModel):
    """Base schema for failure analysis."""
    issue_description: str = Field(..., min_length=10)
    dish_image_url: Optional[str] = None


class FailureAnalysisCreate(FailureAnalysisBase):
    """Schema for creating failure analysis."""
    session_id: UUID


class FailureAnalysisResponse(FailureAnalysisBase):
    """Response schema for failure analysis."""
    id: UUID
    session_id: UUID
    user_id: UUID
    ai_diagnosis: Optional[str] = None
    suggestions: Optional[List[str]] = Field(default_factory=list)
    created_at: datetime
    
    class Config:
        from_attributes = True
