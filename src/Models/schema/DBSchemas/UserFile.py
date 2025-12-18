from .FOcrew_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func, String,JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class UserFile(SQLAlchemyBase):
    __tablename__ = "user_files"

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    file_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    original_filename = Column(String(500), nullable=False)
    file_type = Column(String(10), nullable=False)  
    file_size = Column(Integer, nullable=False) 
    file_path = Column(String(1000), nullable=False)  

    rows_count = Column(Integer, nullable=True)  
    columns_count = Column(Integer, nullable=True)  
    columns_info = Column(JSON, nullable=True)   
    sample_data = Column(JSON, nullable=True)    

    is_processed = Column(Boolean, default=False, nullable=False)
    processing_status = Column(String(50), default="uploaded", nullable=False)
    processing_error = Column(String, nullable=True)

    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.project_id"), nullable=False)
    project = relationship("Project", back_populates="user_files")
