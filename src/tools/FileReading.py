from crewai_tools import FileReadTool,DirectoryReadTool
from crewai.tools import BaseTool
from .Schema import BatchFileReaderSchema
from pydantic import BaseModel
from typing import Type
import pandas as pd


def FileTool():
    file_tool = FileReadTool()
    return file_tool
    
def DirectoryTool():
    directory_tool = DirectoryReadTool()
    return directory_tool


class BatchFileReader(BaseTool):
    name: str = "Batch File Reader"
    description: str = "Reads CSV or Excel files in ~5 equal batches for large file processing."
    args_schema: Type[BaseModel] = BatchFileReaderSchema  

    def _run(self, file_path: str, num_batches: int = 5, mime_type: str = "text/csv"):
        try:
            
            if not mime_type:
                mime_type = "text/csv"

            if num_batches is None:
                num_batches = 5
            # Step 1: Count total rows
            if mime_type == "text/csv":
                total_rows = sum(1 for _ in open(file_path)) - 1  # Exclude header
            elif mime_type in [
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ]:
                df = pd.read_excel(file_path, engine="openpyxl")
                total_rows = df.shape[0]
            else:
                return f"Unsupported MIME type: {mime_type}"

            # Step 2: Determine batch size
            batch_size = max(1, total_rows // num_batches)

            # Step 3: Read in batches
            results = []

            if mime_type == "text/csv":
                reader = pd.read_csv(file_path, chunksize=batch_size)
                for chunk in reader:
                    if not chunk.empty:
                        results.append(chunk.to_dict(orient="records"))

            else:
                # Manual batching for Excel
                for i in range(0, total_rows, batch_size):
                    chunk = df.iloc[i:i+batch_size]
                    if not chunk.empty:
                        results.append(chunk.to_dict(orient="records"))

            return results

        except Exception as e:
            import traceback
            return f"Error reading file: {str(e)}\n{traceback.format_exc()}"
        
