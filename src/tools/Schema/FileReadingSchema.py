from pydantic import BaseModel, Field
from typing import Optional


class BatchFileReaderSchema(BaseModel):
    file_path: str
    num_batches: Optional[int] = Field(default=5)
    mime_type: Optional[str] = Field(default="text/csv")
