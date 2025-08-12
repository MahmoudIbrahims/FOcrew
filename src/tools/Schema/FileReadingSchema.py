from pydantic import BaseModel


class BatchFileReaderSchema(BaseModel):
    file_path: str
    num_batches: int = 15  
    sleep_time: int = 0    
    mime_type: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    max_tokens_per_batch: int = 20000  
    
    

class JsonBatchFileReaderSchema(BaseModel):
    file_path: str  # This should be the path to the directory that contains batch JSON files.
   
