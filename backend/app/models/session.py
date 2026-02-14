"""
Cooking session and failure analysis models
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class SessionStatus(str, enum.Enum):
    """Cooking session status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class StepStatus(str, enum.Enum):
    """Individual step status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class CookingSession(Base):
    """
    Cooking session tracking user's progress through a recipe.
    """
    __tablename__ = "cooking_sessions"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Session Information
    status = Column(Enum(SessionStatus), default=SessionStatus.NOT_STARTED, nullable=False)
    current_step = Column(Integer, default=0, nullable=False)  # Current step number
    
    # Timing
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    paused_at = Column(DateTime(timezone=True), nullable=True)
    total_duration_minutes = Column(Integer, nullable=True)
    
    # Voice Interaction
    voice_enabled = Column(Boolean, default=True, nullable=False)
    voice_commands_count = Column(Integer, default=0, nullable=False)
    
    # AI Assistance
    ai_tips_requested = Column(Integer, default=0, nullable=False)
    ai_questions_asked = Column(Integer, default=0, nullable=False)
    ai_interactions = Column(JSON, nullable=True)  # Store AI conversation history
    
    # Session Notes
    user_notes = Column(Text, nullable=True)
    difficulty_rating = Column(Integer, nullable=True)  # User's difficulty rating (1-5)
    success_rating = Column(Integer, nullable=True)  # How well did it turn out (1-5)
    
    # Demo Mode
    is_demo = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="cooking_sessions")
    recipe = relationship("Recipe", back_populates="cooking_sessions")
    steps = relationship("SessionStep", back_populates="session", cascade="all, delete-orphan", order_by="SessionStep.step_number")
    
    def __repr__(self):
        return f"<CookingSession(id={self.id}, user_id={self.user_id}, recipe_id={self.recipe_id}, status={self.status})>"
    
    @property
    def is_active(self):
        """Check if session is currently active"""
        return self.status in [SessionStatus.IN_PROGRESS, SessionStatus.PAUSED]
    
    @property
    def completion_percentage(self):
        """Calculate completion percentage"""
        if not self.steps:
            return 0
        completed_steps = sum(1 for step in self.steps if step.status == StepStatus.COMPLETED)
        return int((completed_steps / len(self.steps)) * 100) if self.steps else 0


class SessionStep(Base):
    """
    Individual step tracking within a cooking session.
    """
    __tablename__ = "session_steps"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    session_id = Column(Integer, ForeignKey("cooking_sessions.id", ondelete="CASCADE"), nullable=False)
    recipe_step_id = Column(Integer, ForeignKey("recipe_steps.id", ondelete="CASCADE"), nullable=False)
    
    # Step Information
    step_number = Column(Integer, nullable=False)
    status = Column(Enum(StepStatus), default=StepStatus.PENDING, nullable=False)
    
    # Timing
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    # Timer Usage
    timer_used = Column(Boolean, default=False, nullable=False)
    timer_duration_seconds = Column(Integer, nullable=True)
    
    # User Feedback
    was_difficult = Column(Boolean, nullable=True)
    user_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    session = relationship("CookingSession", back_populates="steps")
    recipe_step = relationship("RecipeStep", back_populates="session_steps")
    
    def __repr__(self):
        return f"<SessionStep(session_id={self.session_id}, step_number={self.step_number}, status={self.status})>"


class FailureAnalysis(Base):
    """
    AI-powered analysis of failed dishes with photos and recommendations.
    """
    __tablename__ = "failure_analyses"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="SET NULL"), nullable=True, index=True)
    session_id = Column(Integer, ForeignKey("cooking_sessions.id", ondelete="SET NULL"), nullable=True)
    
    # User Input
    dish_name = Column(String(255), nullable=False)
    user_description = Column(Text, nullable=True)  # What went wrong according to user
    
    # Images
    image_url = Column(Text, nullable=False)  # Cloudinary URL of failed dish
    thumbnail_url = Column(Text, nullable=True)
    
    # AI Analysis
    ai_analysis = Column(Text, nullable=True)  # Detailed AI analysis
    identified_issues = Column(JSON, nullable=True)  # List of identified problems
    recommendations = Column(JSON, nullable=True)  # List of improvement suggestions
    likely_causes = Column(JSON, nullable=True)  # Probable causes of failure
    
    # Confidence & Quality
    ai_confidence_score = Column(Float, nullable=True)  # 0.0 to 1.0
    analysis_quality = Column(String(20), nullable=True)  # "high", "medium", "low"
    
    # AI Model Info
    ai_model = Column(String(50), nullable=True)  # e.g., "gemini-pro-vision"
    ai_model_version = Column(String(50), nullable=True)
    
    # User Feedback
    was_helpful = Column(Boolean, nullable=True)
    user_rating = Column(Integer, nullable=True)  # 1-5 rating
    user_feedback = Column(Text, nullable=True)
    
    # Status
    is_analyzed = Column(Boolean, default=False, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)  # Share with community
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    analyzed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="failure_analyses")
    
    def __repr__(self):
        return f"<FailureAnalysis(id={self.id}, dish_name='{self.dish_name}', is_analyzed={self.is_analyzed})>"
    
    @property
    def has_recommendations(self):
        """Check if analysis has recommendations"""
        return bool(self.recommendations and len(self.recommendations) > 0)
