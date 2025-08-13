from pydantic import BaseModel,Field


class BatchFileReaderSchema(BaseModel):
    file_path: str
    num_batches: int = 50 #15  
    sleep_time: int = 0    
    mime_type: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    max_tokens_per_batch: int = 10000  
    output_directory: str = Field(default="results/Mini_Batches",description="Directory to save batch Json")
    
    

class JsonBatchFileReaderSchema(BaseModel):
    file_path: str  # This should be the path to the directory that contains batch JSON files.
   
