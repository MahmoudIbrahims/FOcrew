from crewai.tools import BaseTool
import pandas as pd

class FileReaderTool(BaseTool):
    name: str = "file_reader_tool"
    description: str = "Reads CSV, Excel, or JSON files into pandas DataFrame and returns Markdown summary."

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

            # Markdown summary
            summary_md = f"### Dataset Summary\n- Shape: {df.shape}\n- Columns & dtypes:\n"
            for col, dtype in df.dtypes.items():
                summary_md += f"  - {col}: {dtype}\n"

            # Missing values
            missing_summary = df.isna().sum()
            summary_md += "\n### Missing Values\n"
            for col, miss in missing_summary.items():
                summary_md += f"- {col}: {miss}\n"

            # Preview
            summary_md += "\n### Preview (Head, Tail, Sample)\n"
            summary_md += "#### Head:\n" + df.head(5).to_markdown() + "\n"
            summary_md += "#### Tail:\n" + df.tail(5).to_markdown() + "\n"
            summary_md += "#### Sample:\n" + df.sample(5).to_markdown() + "\n"

            return summary_md

        except Exception as e:
            return f"⚠️ Error reading file: {str(e)}"
