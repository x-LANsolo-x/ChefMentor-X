"""
Models package - exports all SQLAlchemy models for ChefMentor X

Import this module to access all models:
    from app.models import User, Recipe, CookingSession, etc.
"""
from app.models.user import User
from app.models.profile import UserProfile, SkillLevel
from app.models.recipe import (
    Recipe,
    RecipeIngredient,
    RecipeStep,
    DifficultyLevel,
)
from app.models.session import (
    CookingSession,
    SessionStep,
    FailureAnalysis,
    SessionStatus,
    StepStatus,
)

# Export all models
__all__ = [
    # User models
    "User",
    "UserProfile",
    "SkillLevel",
    
    # Recipe models
    "Recipe",
    "RecipeIngredient",
    "RecipeStep",
    "DifficultyLevel",
    
    # Session models
    "CookingSession",
    "SessionStep",
    "FailureAnalysis",
    "SessionStatus",
    "StepStatus",
]
