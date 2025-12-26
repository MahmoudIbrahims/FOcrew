from crewai.tools import BaseTool
import os

class MarkdownTool(BaseTool):
    name: str = "markdown_writer"
    description: str = "Creates or updates Markdown reports."

    def _run(self, content: str, output_report: str) -> str:
        os.makedirs(os.path.dirname(output_report), exist_ok=True)
        with open(output_report, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Markdown report saved successfully to: {output_report}"
