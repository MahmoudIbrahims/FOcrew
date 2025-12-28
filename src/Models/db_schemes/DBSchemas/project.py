from .FOcrew_base import SQLAlchemyBase
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship


class Project(SQLAlchemyBase):

    __tablename__ = "projects"
    
    project_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    project_name = Column(String(255), nullable=False)
     # Agent Configuration
    company_name = Column(String(255), nullable=True)
    industry_name = Column(String(255), nullable=True)
    report_language = Column(String(50), default="Arabic", nullable=False)
    manager_email = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    user_files = relationship("UserFile", back_populates="project", cascade="all, delete-orphan")