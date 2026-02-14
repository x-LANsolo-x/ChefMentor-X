"""
User and Profile API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.dependencies import get_current_user
from app.db.base import get_db
from app.models.user import User
from app.models.profile import UserProfile
from app.schemas.user import (
    UserResponse,
    UserWithProfile,
    UpdateProfileRequest,
    UserProfileResponse
)

router = APIRouter()


@router.get("/me", response_model=UserWithProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated user with profile.
    
    Returns:
        UserWithProfile: Current user with profile data
    """
    # Fetch user with profile
    result = await db.execute(
        select(User).where(User.id == current_user.id)
    )
    user = result.scalar_one()
    
    # Fetch profile
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()
    
    # Convert to response model
    user_dict = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "profile": profile
    }
    
    return user_dict


@router.put("/me/profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_update: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user's profile.
    
    Args:
        profile_update: Profile update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        UserProfileResponse: Updated profile
    """
    # Get or create profile
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        # Create new profile
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    
    # Update cooking_habits with provided data
    cooking_habits = profile.cooking_habits or {}
    
    update_data = profile_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            cooking_habits[key] = value
    
    profile.cooking_habits = cooking_habits
    
    await db.commit()
    await db.refresh(profile)
    
    return profile


@router.get("/me/preferences", response_model=dict)
async def get_user_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's cooking preferences.
    
    Returns:
        dict: User preferences including dietary restrictions, allergies, etc.
    """
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        return {
            "dietary_restrictions": [],
            "allergies": [],
            "skill_level": "beginner",
            "favorite_cuisines": [],
            "cooking_frequency": None,
            "preferred_cooking_time": None
        }
    
    cooking_habits = profile.cooking_habits or {}
    
    return {
        "dietary_restrictions": cooking_habits.get("dietary_restrictions", []),
        "allergies": cooking_habits.get("allergies", []),
        "skill_level": cooking_habits.get("skill_level", "beginner"),
        "favorite_cuisines": cooking_habits.get("favorite_cuisines", []),
        "cooking_frequency": cooking_habits.get("cooking_frequency"),
        "preferred_cooking_time": cooking_habits.get("preferred_cooking_time")
    }


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete current user's account (soft delete).
    
    Note: This performs a soft delete by setting is_active to False.
    """
    current_user.is_active = False
    await db.commit()
    
    return None
