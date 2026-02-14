"""
ChefMentor X – Audit Log Model

Tracks important user actions for analytics and debugging.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Action tracking
    action = Column(String(100), nullable=False)  # e.g., cook_start, cook_complete, analysis_upload
    resource_type = Column(String(50))  # e.g., recipe, session, analysis
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Details
    details = Column(JSONB, default={})  # Renamed from 'metadata' to avoid SQLAlchemy conflict
    ip_address = Column(String(45), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
