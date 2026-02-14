from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, Text, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.base import Base
import enum

# Define Python Enum for difficulty levels
class DifficultyLevel(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Core Fields
    title = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=True)  # Alias for backward compatibility
    description = Column(Text, nullable=True)
    difficulty = Column(ENUM(DifficultyLevel, name='difficultylevel', create_type=False), nullable=True)
    
    # Time fields
    prep_time_minutes = Column(Integer, nullable=True)
    cook_time_minutes = Column(Integer, nullable=True)
    total_time_minutes = Column(Integer, nullable=True)
    
    # Servings & Nutrition
    servings = Column(Integer, nullable=False, default=1)
    calories = Column(Integer, nullable=True)
    protein_grams = Column(Float, nullable=True)
    carbs_grams = Column(Float, nullable=True)
    fat_grams = Column(Float, nullable=True)
    
    # Categorization
    cuisine_type = Column(String(100), nullable=True)
    meal_type = Column(String(100), nullable=True)
    tags = Column(JSON, nullable=True)
    
    # External API Links (RecipeDB)
    image_url = Column(Text, nullable=True)
    
    # Status flags
    is_active = Column(Boolean, nullable=False, default=True)
    is_featured = Column(Boolean, nullable=False, default=False)
    ai_generated = Column(Boolean, nullable=False, default=False)
    ai_model = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    steps = relationship("RecipeStep", back_populates="recipe", order_by="RecipeStep.step_number", cascade="all, delete-orphan")
    cooking_sessions = relationship("CookingSession", back_populates="recipe")

class RecipeStep(Base):
    __tablename__ = "recipe_steps"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey('recipes.id'), nullable=False, index=True)
    
    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)
    instruction = Column(Text, nullable=False)
    expected_state = Column(String(255), nullable=True)  # For tests and cooking guidance
    duration_minutes = Column(Integer, nullable=True)
    timer_required = Column(Boolean, nullable=False, default=False)
    image_url = Column(Text, nullable=True)
    video_url = Column(Text, nullable=True)
    ai_tips = Column(Text, nullable=True)
    common_mistakes = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    recipe = relationship("Recipe", back_populates="steps")
