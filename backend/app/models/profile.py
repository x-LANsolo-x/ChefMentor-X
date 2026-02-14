"""
User profile model for storing preferences and cooking history
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class SkillLevel(str, enum.Enum):
    """User cooking skill level"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class UserProfile(Base):
    """
    Extended user profile with cooking preferences and history.
    """
    __tablename__ = "user_profiles"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key (One-to-One with User)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # Cooking Preferences
    skill_level = Column(Enum(SkillLevel), default=SkillLevel.BEGINNER, nullable=False)
    preferred_cuisines = Column(JSON, nullable=True)  # List: ["Italian", "Mexican"]
    dietary_restrictions = Column(JSON, nullable=True)  # List: ["vegetarian", "gluten-free"]
    allergies = Column(JSON, nullable=True)  # List: ["peanuts", "shellfish"]
    
    # Voice & Interaction Preferences
    voice_speed = Column(String(20), default="normal", nullable=False)  # "slow", "normal", "fast"
    voice_volume = Column(Integer, default=80, nullable=False)  # 0-100
    preferred_voice = Column(String(50), nullable=True)  # Voice ID for TTS
    auto_timer = Column(Boolean, default=True, nullable=False)  # Auto-start timers
    
    # Display Preferences
    measurement_system = Column(String(20), default="metric", nullable=False)  # "metric" or "imperial"
    theme = Column(String(20), default="light", nullable=False)  # "light", "dark", "auto"
    font_size = Column(String(20), default="medium", nullable=False)  # "small", "medium", "large"
    
    # Cooking Stats
    total_sessions = Column(Integer, default=0, nullable=False)
    completed_sessions = Column(Integer, default=0, nullable=False)
    total_cooking_time_minutes = Column(Integer, default=0, nullable=False)
    favorite_recipes = Column(JSON, nullable=True)  # List of recipe IDs
    
    # Achievement & Progress
    recipes_mastered = Column(Integer, default=0, nullable=False)
    current_streak_days = Column(Integer, default=0, nullable=False)
    longest_streak_days = Column(Integer, default=0, nullable=False)
    achievements = Column(JSON, nullable=True)  # List of achievement IDs/badges
    
    # AI Interaction Stats
    total_ai_questions = Column(Integer, default=0, nullable=False)
    total_voice_commands = Column(Integer, default=0, nullable=False)
    ai_helpfulness_rating = Column(Integer, nullable=True)  # Average rating
    
    # Personalization
    learning_style = Column(String(50), nullable=True)  # "visual", "audio", "kinesthetic"
    bio = Column(Text, nullable=True)  # User bio/description
    location = Column(String(255), nullable=True)  # City, Country
    
    # Notifications
    email_notifications = Column(Boolean, default=True, nullable=False)
    push_notifications = Column(Boolean, default=True, nullable=False)
    cooking_reminders = Column(Boolean, default=False, nullable=False)
    
    # Privacy
    profile_visibility = Column(String(20), default="private", nullable=False)  # "public", "friends", "private"
    share_cooking_history = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_active = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, skill_level={self.skill_level})>"
    
    @property
    def completion_rate(self):
        """Calculate session completion rate"""
        if self.total_sessions == 0:
            return 0
        return int((self.completed_sessions / self.total_sessions) * 100)
    
    @property
    def average_cooking_time(self):
        """Calculate average cooking time per session"""
        if self.completed_sessions == 0:
            return 0
        return int(self.total_cooking_time_minutes / self.completed_sessions)
