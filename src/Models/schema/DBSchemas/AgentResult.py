from .FOcrew_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func, String, Text, JSON, Boolean, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship



class AgentResult(SQLAlchemyBase):
    
    __tablename__ = "agent_results"
    
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    result_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    
    agent_name = Column(String(255), nullable=False)
    agent_type = Column(String, nullable=False, default="generic")
    task_description = Column(Text, nullable=True)
    
 
    result_data = Column(JSON, nullable=True)  
    result_text = Column(Text, nullable=True)  
    status = Column(String(50), default="completed", nullable=False) 
    
   
    execution_time = Column(Float, nullable=True)  
    tokens_used = Column(Integer, nullable=True)  
    cost = Column(Float, nullable=True)  
    
    agent_metadata = Column(JSON, nullable=True) 
    error_message = Column(Text, nullable=True)  
    
    
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
  
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    project = relationship("Project", back_populates="agent_results")
