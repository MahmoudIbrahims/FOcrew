from crewai_tools import FileReadTool,DirectoryReadTool
from crewai.tools import BaseTool
import pandas as pd
import os

def FileTool():
    file_tool = FileReadTool()
    return file_tool
    
def DirectoryTool():
    directory_tool = DirectoryReadTool()
    return directory_tool


class BatchFileReader(BaseTool):
    name: str = "Batch File Reader"
    description: str = "Reads CSV or Excel files in ~5 equal batches for large file processing."

    def _run(self, file_path: str, num_batches: int = 5, mime_type: str = "text/csv"):
        try:
            # Step 1: Count total rows
            if mime_type == "text/csv":
                total_rows = sum(1 for _ in open(file_path)) - 1  # minus header
            elif mime_type in [
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ]:
                total_rows = pd.read_excel(file_path, engine="openpyxl").shape[0]
            else:
                return f"Unsupported MIME type: {mime_type}"

            # Step 2: Determine batch size
            batch_size = max(1, total_rows // num_batches)

            # Step 3: Read in batches
            if mime_type == "text/csv":
                reader = pd.read_csv(file_path, chunksize=batch_size)
            else:
                reader = pd.read_excel(file_path, chunksize=batch_size, engine="openpyxl")

            # Step 4: Store results
            results = []
            for i, chunk in enumerate(reader):
                if chunk.empty:
                    continue
                results.append(chunk.to_dict(orient="records"))

            return results

        except Exception as e:
            import traceback
            return f"Error reading file: {str(e)}\n{traceback.format_exc()}"


