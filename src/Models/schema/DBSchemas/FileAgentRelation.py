from .FOcrew_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func, String, Text, JSON, Boolean, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship


class FileAgentRelation(SQLAlchemyBase):
    
    __tablename__ = "file_agent_relations"
    
    relation_id = Column(Integer, primary_key=True, autoincrement=True)
    
    
    file_id = Column(Integer, ForeignKey("user_files.file_id"), nullable=False)
    agent_result_id = Column(Integer, ForeignKey("agent_results.result_id"), nullable=False)
    
   
    usage_type = Column(String(100), nullable=False)  # input, output, reference
    usage_description = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
   
    user_file = relationship("UserFile")
    agent_result = relationship("AgentResult")