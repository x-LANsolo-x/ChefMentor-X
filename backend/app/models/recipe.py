"""
Recipe models for storing recipes, ingredients, and cooking steps
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class DifficultyLevel(str, enum.Enum):
    """Recipe difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Recipe(Base):
    """
    Recipe model containing recipe information and metadata.
    """
    __tablename__ = "recipes"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    
    # Metadata
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.BEGINNER, nullable=False)
    prep_time_minutes = Column(Integer, nullable=True)  # Preparation time
    cook_time_minutes = Column(Integer, nullable=True)  # Cooking time
    total_time_minutes = Column(Integer, nullable=True)  # Total time
    servings = Column(Integer, default=1, nullable=False)
    
    # Nutritional Info (optional)
    calories = Column(Integer, nullable=True)
    protein_grams = Column(Float, nullable=True)
    carbs_grams = Column(Float, nullable=True)
    fat_grams = Column(Float, nullable=True)
    
    # Categories & Tags
    cuisine_type = Column(String(100), nullable=True)  # e.g., "Italian", "Chinese"
    meal_type = Column(String(100), nullable=True)  # e.g., "breakfast", "dinner"
    tags = Column(JSON, nullable=True)  # List of tags: ["vegetarian", "gluten-free"]
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    
    # AI Generation Info
    ai_generated = Column(Boolean, default=False, nullable=False)
    ai_model = Column(String(50), nullable=True)  # e.g., "gemini-pro"
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan", order_by="RecipeIngredient.order")
    steps = relationship("RecipeStep", back_populates="recipe", cascade="all, delete-orphan", order_by="RecipeStep.step_number")
    cooking_sessions = relationship("CookingSession", back_populates="recipe")
    
    def __repr__(self):
        return f"<Recipe(id={self.id}, title='{self.title}', difficulty={self.difficulty})>"
    
    @property
    def total_ingredients(self):
        """Get total number of ingredients"""
        return len(self.ingredients) if self.ingredients else 0
    
    @property
    def total_steps(self):
        """Get total number of steps"""
        return len(self.steps) if self.steps else 0


class RecipeIngredient(Base):
    """
    Recipe ingredients with quantities and units.
    """
    __tablename__ = "recipe_ingredients"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    
    # Ingredient Information
    name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=True)  # e.g., 2.5
    unit = Column(String(50), nullable=True)  # e.g., "cups", "grams", "pieces"
    notes = Column(Text, nullable=True)  # e.g., "chopped", "room temperature"
    
    # Ordering
    order = Column(Integer, default=0, nullable=False)
    
    # Optional categorization
    category = Column(String(100), nullable=True)  # e.g., "main", "spices", "garnish"
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    recipe = relationship("Recipe", back_populates="ingredients")
    
    def __repr__(self):
        return f"<RecipeIngredient(recipe_id={self.recipe_id}, name='{self.name}', quantity={self.quantity} {self.unit})>"
    
    @property
    def display_text(self):
        """Get formatted ingredient text"""
        parts = []
        if self.quantity:
            parts.append(str(self.quantity))
        if self.unit:
            parts.append(self.unit)
        parts.append(self.name)
        if self.notes:
            parts.append(f"({self.notes})")
        return " ".join(parts)


class RecipeStep(Base):
    """
    Cooking steps for recipes with instructions and timing.
    """
    __tablename__ = "recipe_steps"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    
    # Step Information
    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)  # Optional step title
    instruction = Column(Text, nullable=False)
    
    # Timing
    duration_minutes = Column(Integer, nullable=True)  # Time for this step
    timer_required = Column(Boolean, default=False, nullable=False)
    
    # Media
    image_url = Column(Text, nullable=True)  # Optional step image
    video_url = Column(Text, nullable=True)  # Optional step video
    
    # AI Tips
    ai_tips = Column(Text, nullable=True)  # AI-generated cooking tips for this step
    common_mistakes = Column(JSON, nullable=True)  # List of common mistakes to avoid
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    recipe = relationship("Recipe", back_populates="steps")
    session_steps = relationship("SessionStep", back_populates="recipe_step")
    
    def __repr__(self):
        return f"<RecipeStep(recipe_id={self.recipe_id}, step_number={self.step_number})>"
    
    @property
    def display_title(self):
        """Get step title or generate one"""
        return self.title or f"Step {self.step_number}"
