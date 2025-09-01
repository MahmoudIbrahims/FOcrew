from pydantic import BaseModel, Field

class MarkdownToPDFSchema(BaseModel):
    file_path: str = Field(..., description="Path to the input Markdown file")
    logo_path: str = Field(..., description="Path to the logo image")
    output_pdf: str = Field(default="report.pdf", description="Output PDF file path")
