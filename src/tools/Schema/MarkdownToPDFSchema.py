from pydantic import BaseModel, Field
from typing import Optional 

class MarkdownToPDFSchema(BaseModel):
    file_path: str = Field(..., description="Path to the input Markdown file")
    output_report: str = Field(default="report.pdf", description="Output PDF file path")
