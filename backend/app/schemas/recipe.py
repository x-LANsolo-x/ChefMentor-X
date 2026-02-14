"""
Recipe schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class RecipeStepBase(BaseModel):
    """Base schema for recipe step"""
    step_number: int = Field(..., ge=1, description="Step number (starting from 1)")
    instruction: str = Field(..., min_length=1, description="Step instruction text")
    expected_state: Optional[str] = Field(None, description="Expected visual/sensory state")


class RecipeStepCreate(RecipeStepBase):
    """Schema for creating a recipe step"""
    pass


class RecipeStepResponse(RecipeStepBase):
    """Schema for recipe step response"""
    id: UUID
    recipe_id: UUID
    
    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    """Base schema for recipe"""
    name: str = Field(..., min_length=1, max_length=255, description="Recipe name")
    difficulty: Optional[str] = Field(None, description="Difficulty level: easy, medium, hard")
    estimated_time_min: Optional[int] = Field(None, ge=1, description="Estimated time in minutes")
    external_id: Optional[str] = Field(None, description="External recipe database ID")
    source_url: Optional[str] = Field(None, description="Source URL")
    image_url: Optional[str] = Field(None, description="Recipe image URL")


class RecipeCreate(RecipeBase):
    """Schema for creating a recipe"""
    steps: List[RecipeStepCreate] = Field(default_factory=list, description="Recipe steps")


class RecipeUpdate(BaseModel):
    """Schema for updating a recipe"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    difficulty: Optional[str] = None
    estimated_time_min: Optional[int] = Field(None, ge=1)
    image_url: Optional[str] = None


class RecipeListItem(RecipeBase):
    """Schema for recipe in list view (without steps)"""
    id: UUID
    created_at: datetime
    step_count: int = Field(default=0, description="Number of steps")
    
    class Config:
        from_attributes = True


class RecipeDetail(RecipeBase):
    """Schema for detailed recipe view (with steps)"""
    id: UUID
    created_at: datetime
    steps: List[RecipeStepResponse] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class RecipeSearchParams(BaseModel):
    """Schema for recipe search parameters"""
    query: Optional[str] = Field(None, description="Search query")
    difficulty: Optional[str] = Field(None, description="Filter by difficulty")
    max_time_min: Optional[int] = Field(None, ge=1, description="Maximum time in minutes")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class RecipeListResponse(BaseModel):
    """Schema for paginated recipe list response"""
    recipes: List[RecipeListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
