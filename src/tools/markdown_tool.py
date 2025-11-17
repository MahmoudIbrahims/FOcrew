from crewai.tools import BaseTool
import os

class MarkdownTool(BaseTool):
    name: str = "markdown_writer"
    description: str = "Creates or updates Markdown reports."

    def _run(self, content: str, output_path: str = "results/Data_Analysis/Analysis_Report.md") -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Markdown report saved successfully to: {output_path}"
