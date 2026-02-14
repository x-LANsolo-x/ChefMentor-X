"""
User model for authentication and profile management
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    """
    User model for authentication and user management.
    
    Supports both authenticated users (OAuth) and demo/guest users.
    """
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=True)  # For future email/password auth
    
    # OAuth Information
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    oauth_provider = Column(String(50), nullable=True)  # 'google', 'apple', etc.
    
    # User Type
    is_active = Column(Boolean, default=True, nullable=False)
    is_demo = Column(Boolean, default=False, nullable=False)  # True for demo users
    is_admin = Column(Boolean, default=False, nullable=False)
    
    # Profile Information
    full_name = Column(String(255), nullable=True)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(Text, nullable=True)
    
    # Preferences
    language = Column(String(10), default='en', nullable=False)
    voice_enabled = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    cooking_sessions = relationship("CookingSession", back_populates="user", cascade="all, delete-orphan")
    failure_analyses = relationship("FailureAnalysis", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, is_demo={self.is_demo})>"
    
    @property
    def is_authenticated(self):
        """Check if user is authenticated (not demo)"""
        return not self.is_demo and self.is_active
    
    @property
    def name(self):
        """Get display name or fallback to email"""
        return self.display_name or self.full_name or self.email or f"User {self.id}"
