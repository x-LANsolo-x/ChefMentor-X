from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid as uuid_pkg

class StartCookingRequest(BaseModel):
    recipe_id: str = Field(..., description="Recipe ID to start cooking")
    demo_session_id: Optional[str] = Field(None, description="Demo session ID for guest mode")

class CookingSessionResponse(BaseModel):
    id: uuid_pkg.UUID
    recipe_id: uuid_pkg.UUID
    status: str
    current_step_index: str
    started_at: datetime
    
    class Config:
        from_attributes = True

class StepResponse(BaseModel):
    step_number: int
    instruction: str
    expected_state: Optional[str] = None
    is_last_step: bool = False
    guidance: Optional[str] = None  # For AI tips later
    message: Optional[str] = None  # For completion message
