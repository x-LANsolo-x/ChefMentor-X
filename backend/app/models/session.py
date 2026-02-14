from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid
from app.db.base import Base

class DemoSession(Base):
    __tablename__ = "demo_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24), nullable=False)

class CookingSession(Base):
    __tablename__ = "cooking_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Link to User (is_demo flag for guest mode)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    
    # State
    status = Column(Enum('NOT_STARTED', 'IN_PROGRESS', 'PAUSED', 'COMPLETED', 'ABANDONED', name='sessionstatus'), default='IN_PROGRESS')
    current_step = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    paused_at = Column(DateTime, nullable=True)
    total_duration_minutes = Column(Integer, nullable=True)
    
    # Voice & AI Tracking
    voice_enabled = Column(Boolean, default=False)
    voice_commands_count = Column(Integer, default=0)
    ai_tips_requested = Column(Integer, default=0)
    ai_questions_asked = Column(Integer, default=0)
    ai_interactions = Column(JSON, nullable=True)
    
    # User Feedback
    user_notes = Column(Text, nullable=True)
    difficulty_rating = Column(Integer, nullable=True)  # 1-5
    success_rating = Column(Integer, nullable=True)  # 1-5
    
    # Demo mode
    is_demo = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="cooking_sessions")
    recipe = relationship("Recipe", back_populates="cooking_sessions")

class FailureAnalysis(Base):
    __tablename__ = "failure_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    cooking_session_id = Column(Integer, ForeignKey('cooking_sessions.id'), nullable=True)
    
    media_url = Column(Text, nullable=False)  # Cloudinary URL
    root_cause = Column(Text)
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="failure_analyses")
