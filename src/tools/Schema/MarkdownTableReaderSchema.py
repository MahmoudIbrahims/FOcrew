from pydantic import BaseModel,Field

class MarkdownTableReaderSchema(BaseModel):
    file_path: str
    output_dir: str = Field(default="results/Dashboard",description="Directory to save file HTML")
    