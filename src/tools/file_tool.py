from crewai.tools import BaseTool
import pandas as pd

class FileReaderTool(BaseTool):
    name: str = "file_reader_tool"
    description: str = "Reads CSV, Excel, or JSON files into pandas DataFrame."

    def _run(self, file_path: str) -> str:
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            elif file_path.endswith(".json"):
                df = pd.read_json(file_path)
            else:
                return "❌ Unsupported file type."
            
            info = df.info(buf=None)
            return f"✅ File loaded successfully:\n{info}\n\n{df.head().to_string()}"
        except Exception as e:
            return f"⚠️ Error reading file: {str(e)}"
