from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid
from app.db.base import Base

class DemoSession(Base):
    __tablename__ = "demo_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24), nullable=False)
    
    # Relationships
    cooking_sessions = relationship("CookingSession", back_populates="demo_session")
    failure_analyses = relationship("FailureAnalysis", back_populates="demo_session")

class CookingSession(Base):
    __tablename__ = "cooking_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Link to User OR Demo Session
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    demo_session_id = Column(UUID(as_uuid=True), ForeignKey('demo_sessions.id'), nullable=True)
    
    # Link to Recipe
    recipe_id = Column(UUID(as_uuid=True), ForeignKey('recipes.id'), nullable=False)
    
    # State
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default='in_progress') # in_progress, completed, abandoned
    current_step_index = Column(String(50), default='0') # Track progress
    
    # Caching AI (Prefetching)
    next_step_guidance = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="cooking_sessions")
    demo_session = relationship("DemoSession", back_populates="cooking_sessions")
    recipe = relationship("Recipe", back_populates="cooking_sessions")

class FailureAnalysis(Base):
    __tablename__ = "failure_analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    demo_session_id = Column(UUID(as_uuid=True), ForeignKey('demo_sessions.id'), nullable=True)
    
    media_url = Column(Text, nullable=False) # Cloudinary URL
    root_cause = Column(Text)
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="failure_analyses")
    demo_session = relationship("DemoSession", back_populates="failure_analyses")
