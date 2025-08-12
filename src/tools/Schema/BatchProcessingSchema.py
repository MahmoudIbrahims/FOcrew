
from pydantic import BaseModel, Field
from pathlib import Path

class BatchProcessorSchema(BaseModel):
    """Input schema for BatchProcessor."""
    input_directory: str = Field(..., description="Path to the directory containing batch JSON files")
    output_directory: str = Field(default="results/Mini_reports",description="Directory to save batch reports")
    final_report_path: str = Field(default="results/inventory_management/data_analysis_report.md",description="Path for the final consolidated report")
   

