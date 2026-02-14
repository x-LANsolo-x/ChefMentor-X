"""
User and Profile schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a user"""
    pass


class UserResponse(UserBase):
    """Schema for user response"""
    id: UUID
    role: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileBase(BaseModel):
    """Base user profile schema"""
    cooking_habits: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="User cooking preferences and habits"
    )


class UserProfileCreate(UserProfileBase):
    """Schema for creating user profile"""
    pass


class UserProfileUpdate(UserProfileBase):
    """Schema for updating user profile"""
    cooking_habits: Optional[Dict[str, Any]] = None


class UserProfileResponse(UserProfileBase):
    """Schema for user profile response"""
    id: UUID
    user_id: UUID
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserWithProfile(UserResponse):
    """Schema for user with profile data"""
    profile: Optional[UserProfileResponse] = None


class UpdateProfileRequest(BaseModel):
    """Schema for profile update request"""
    dietary_restrictions: Optional[list[str]] = Field(None, description="e.g., ['vegetarian', 'gluten-free']")
    allergies: Optional[list[str]] = Field(None, description="e.g., ['peanuts', 'shellfish']")
    skill_level: Optional[str] = Field(None, description="beginner, intermediate, advanced")
    favorite_cuisines: Optional[list[str]] = Field(None, description="e.g., ['italian', 'indian']")
    cooking_frequency: Optional[str] = Field(None, description="daily, weekly, monthly")
    preferred_cooking_time: Optional[int] = Field(None, ge=1, description="Preferred cooking time in minutes")


# Demo Session Schemas
class DemoSessionCreate(BaseModel):
    """Schema for creating a demo session"""
    device_id: str = Field(..., description="Unique device identifier")


class DemoSessionResponse(BaseModel):
    """Response schema for demo session"""
    id: int
    device_id: str
    session_token: str
    is_active: bool
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
