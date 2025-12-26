import logging
from typing import Dict, Type
from crewai.tools import BaseTool
from pydantic import BaseModel
from markdown_it import MarkdownIt
from weasyprint import HTML
from bs4 import BeautifulSoup
from datetime import datetime
from .Schema.MarkdownToPDFSchema import MarkdownToPDFSchema


class MarkdownToPDFReport(BaseTool):
    name: str = "Markdown to PDF Report Generator"
    description: str = "Converts a Markdown file into a styled PDF report with logo, cover page, table of contents, and cleaned tables."
    args_schema: Type[BaseModel] = MarkdownToPDFSchema
    
    def _run(
        self,
        file_path: str  ,#="results/Data_Analysis/Analysis_Report.md",            
        output_report: str #= "results/Data_Analysis/Analysis_Report.pdf"
        
    ) -> Dict[str, str]:
        try:
            # 1. Read Markdown file
            with open(file_path, "r", encoding="utf-8") as f:
                markdown_text = f.read()

            # 2. Convert Markdown → HTML
            md = MarkdownIt().enable("table")
            html_content = md.render(markdown_text)

            # 3. Clean tables (normalize column counts only, no merging)
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

            # --- 4. Build Table of Contents (TOC) ---
            toc_items = []
            headers = soup.find_all(["h1", "h2", "h3"])
            for i, header in enumerate(headers):
                anchor_id = f"section-{i}"
                header["id"] = anchor_id
                indent = "20px" if header.name == "h2" else ("40px" if header.name == "h3" else "0px")
                toc_items.append(f'<div style="margin-left:{indent}"><a href="#{anchor_id}">{header.text}</a></div>')

            toc_html = """
            <div class="toc">
                <h2>Table of Contents</h2>
                {}
            </div>
            <div style="page-break-after: always;"></div>
            """.format("\n".join(toc_items))

            # Update HTML content after cleaning and TOC
            html_content = str(soup)

            # Current date
            report_date = datetime.now().strftime("%B %d, %Y")

            # 5. Create full HTML with cover + TOC + report
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
                    margin: 20px 0;
                    table-layout: auto;
                    border: 1px solid #444;
                    font-size: 12px;
                }}
                th, td {{
                    border: 1px solid #444;
                    padding: 6px;
                    text-align: left;
                    word-wrap: break-word;
                    white-space: normal;
                    vertical-align: top;
                    page-break-inside: avoid;
                }}
                th {{
                    background: #f4f4f4;
                }}
                tr:nth-child(even) {{
                    background: #fafafa;
                }}
                .cover {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    text-align: center;
                }}
                .cover img {{
                    height: 100px;
                    margin-bottom: 20px;
                }}
                .cover h1 {{
                    font-size: 36px;
                    margin-bottom: 20px;
                }}
                .cover p {{
                    font-size: 16px;
                    color: #555;
                }}
                .toc {{
                    margin-top: 40px;
                }}
                .toc h2 {{
                    font-size: 24px;
                    margin-bottom: 20px;
                }}
                .toc a {{
                    text-decoration: none;
                    color: #2c3e50;
                }}
                .toc a:hover {{
                    text-decoration: underline;
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
                <!-- Cover Page -->
                <div class="cover">
                    <img src="../docs/logo.png" alt="Company Logo"> 
                    <h1>Analysis Report</h1>
                    <p>Date: {report_date}</p>
                </div>

                <div style="page-break-after: always;"></div>

                <!-- TOC -->
                {toc_html}

                <!-- Report Content -->
                <div class="header">
                    <img src="../docs/logo.png" alt="Company Logo"> 
                    <h1>Analysis Report</h1>
                </div>

                {html_content}

                <div class="footer">
                    © 2025 FOcrew. All rights reserved.
                </div>
            </body>
            </html>
            """

            # 6. Export as PDF
            HTML(string=html_with_logo, base_url=".").write_pdf(output_report)

            logging.info(f"PDF report generated at: {output_report}")
            return {"status": "success", "output_pdf": output_report}

        except Exception as e:
            logging.error(f"Error generating PDF: {e}")
            return {"status": "error", "message": str(e)}
