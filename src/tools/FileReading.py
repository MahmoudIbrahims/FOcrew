from crewai_tools import FileReadTool,DirectoryReadTool
from crewai.tools import BaseTool
from .Schema import BatchFileReaderSchema
from pydantic import BaseModel
from typing import Type ,Optional
import pandas as pd
import numpy as np
import os

def FileTool():
    file_tool = FileReadTool()
    return file_tool
    
def DirectoryTool():
    directory_tool = DirectoryReadTool()
    return directory_tool


# class BatchFileReader(BaseTool):
#     name: str = "Batch File Reader"
#     description: str = "Reads CSV or Excel files in ~5 equal batches for large file processing."
#     args_schema: Type[BaseModel] = BatchFileReaderSchema  

#     def _run(self, file_path: str, num_batches: int = 5, mime_type: str = "text/csv"):
#         try:
            
#             if not mime_type:
#                 mime_type = "text/csv"

#             if num_batches is None:
#                 num_batches = 5
#             # Step 1: Count total rows
#             if mime_type == "text/csv":
#                 total_rows = sum(1 for _ in open(file_path)) - 1  # Exclude header
#             elif mime_type in [
#                 "application/vnd.ms-excel",
#                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             ]:
#                 df = pd.read_excel(file_path, engine="openpyxl")
#                 total_rows = df.shape[0]
#             else:
#                 return f"Unsupported MIME type: {mime_type}"

#             # Step 2: Determine batch size
#             batch_size = max(1, total_rows // num_batches)

#             # Step 3: Read in batches
#             results = []

#             if mime_type == "text/csv":
#                 reader = pd.read_csv(file_path, chunksize=batch_size,encoding="utf-8")
#                 for chunk in reader:
#                     if not chunk.empty:
#                         results.append(chunk.to_dict(orient="records"))

#             else:
#                 # Manual batching for Excel
#                 for i in range(0, total_rows, batch_size):
#                     chunk = df.iloc[i:i+batch_size]
#                     if not chunk.empty:
#                         results.append(chunk.to_dict(orient="records"))

#             return results

#         except Exception as e:
#             import traceback
#             return f"Error reading file: {str(e)}\n{traceback.format_exc()}"

        
class BatchFileReader(BaseTool):
    name: str = "Batch File Reader"
    description: str = "Reads CSV or Excel files in ~5 equal batches for large file processing."
    args_schema: Type[BaseModel] = BatchFileReaderSchema  

    def _run(self, file_path: str, num_batches: int = 5, mime_type: Optional[str] = None):
        try:
            ext = os.path.splitext(file_path)[1].lower()

            if mime_type is None:
                if ext == '.csv':
                    mime_type = "text/csv"
                elif ext in ['.xls', '.xlsx']:
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            if mime_type == "text/csv":
                df = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip', engine="python")
            elif mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                try:
                    import openpyxl
                    df = pd.read_excel(file_path, engine="openpyxl")
                except ImportError:
                    return "❌ Error: `openpyxl` is required for reading Excel files. Install it via `pip install openpyxl`"
            else:
                return f"❌ Unsupported MIME type or file extension: {mime_type}"

            if df.empty:
                return "⚠️ Warning: Loaded DataFrame is empty."

            # Split into batches
            batches = np.array_split(df, num_batches or 5)
            batch_results = [batch.to_dict(orient='records') for batch in batches]
            return batch_results

        except Exception as e:
            import traceback
            return f"❌ Error reading file: {e}\n{traceback.format_exc()}"
