from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class StartCookingRequest(BaseModel):
    recipe_id: int = Field(..., description="Recipe ID to start cooking")
    is_demo: bool = Field(False, description="Is this a demo/guest session")

class CookingSessionResponse(BaseModel):
    id: int
    recipe_id: int
    status: str
    current_step: int
    started_at: datetime
    is_demo: bool
    
    class Config:
        from_attributes = True

class StepResponse(BaseModel):
    step_number: int
    instruction: str
    expected_state: Optional[str] = None
    is_last_step: bool = False
    guidance: Optional[str] = None  # For AI tips later
    message: Optional[str] = None  # For completion message
