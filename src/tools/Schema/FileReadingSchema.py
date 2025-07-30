from pydantic import BaseModel


class BatchFileReaderSchema(BaseModel):
    file_path: str
    num_batches: int = 20 
    sleep_time: int = 5    
    mime_type: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    max_tokens_per_batch: int = 500
    
   
