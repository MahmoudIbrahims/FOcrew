import logging
from typing import Dict, Type
from crewai.tools import BaseTool
from pydantic import BaseModel
from markdown_it import MarkdownIt
from weasyprint import HTML
from bs4 import BeautifulSoup
from .Schema.MarkdownToPDFSchema import MarkdownToPDFSchema

#Tool
class MarkdownToPDFReport(BaseTool):
    name: str = "Markdown to PDF Report Generator"
    description: str = "Converts a Markdown file into a styled PDF report with logo and cleaned tables."
    args_schema: Type[BaseModel] = MarkdownToPDFSchema

    def _run(self, file_path: str ="results/inventory_management/Analysis_Report.md",
            logo_path: str = None,
            output_pdf: str = "results/inventory_management/report.pdf") -> Dict[str, str]:
        try:
            # 1. Read Markdown file
            with open(file_path, "r", encoding="utf-8") as f:
                markdown_text = f.read()

            # 2. Convert Markdown → HTML
            md = MarkdownIt().enable("table")
            html_content = md.render(markdown_text)

            # 3. Clean tables (normalize column counts & merge if needed)
            soup = BeautifulSoup(html_content, "html.parser")

            for table in soup.find_all("table"):
                max_cols = 0
                for row in table.find_all("tr"):
                    cols = len(row.find_all(["td", "th"]))
                    if cols > max_cols:
                        max_cols = cols

                for row in table.find_all("tr"):
                    cells = row.find_all(["td", "th"])
                    diff = max_cols - len(cells)
                    if diff > 0:
                        for _ in range(diff):
                            empty_cell = soup.new_tag("td")
                            empty_cell.string = "\u00A0"
                            row.append(empty_cell)

            tables = soup.find_all("table")
            i = 0
            while i < len(tables) - 1:
                current = tables[i]
                nxt = tables[i + 1]

                current_cols = len(current.find("tr").find_all(["td", "th"])) if current.find("tr") else 0
                next_cols = len(nxt.find("tr").find_all(["td", "th"])) if nxt.find("tr") else 0

                if current_cols == next_cols and current_cols > 0:
                    for row in nxt.find_all("tr"):
                        current.append(row.extract())
                    nxt.decompose()
                    tables = soup.find_all("table")
                else:
                    i += 1

            html_content = str(soup)

            # 4. Inject logo + styling
            html_with_logo = f"""
            <html>
            <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    line-height: 1.6;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                    table-layout: auto;
                }}
                th, td {{
                    border: 1px solid #444;
                    padding: 8px;
                    text-align: left;
                    word-wrap: break-word;
                    white-space: normal;
                    vertical-align: top;
                }}
                th {{
                    background: #f4f4f4;
                }}
                .header {{
                    display: flex;
                    align-items: center;
                    margin-bottom: 40px;
                }}
                .header img {{
                    height: 60px;
                    margin-right: 20px;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    margin-top: 40px;
                    color: #888;
                }}
            </style>
            </head>
            <body>
                <div class="header">
                    <img src="{logo_path}" alt="Company Logo">
                    <h1>Inventory Report</h1>
                </div>

                {html_content}

                <div class="footer">
                    © 2025 Company Name. All rights reserved.
                </div>
            </body>
            </html>
            """

            # 5. Export as PDF
            HTML(string=html_with_logo, base_url=".").write_pdf(output_pdf)

            logging.info(f"PDF report generated at: {output_pdf}")
            return {"status": "success", "output_pdf": output_pdf}

        except Exception as e:
            logging.error(f"Error generating PDF: {e}")
            return {"status": "error", "message": str(e)}
