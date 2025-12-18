from pydantic import BaseModel, EmailStr
from typing import Optional


class ProjectCreateRequest(BaseModel):
    project_name: str  # Required
    company_name: Optional[str] = None  # Optional
    industry_name: Optional[str] = None  # Optional
    report_language: Optional[str] = "Arabic"  # Optional with default
    manager_email: Optional[EmailStr] = None  # Optional with email validation