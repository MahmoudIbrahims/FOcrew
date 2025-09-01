from string import Template

description_prompt =Template("\n".join([
            "Take the Markdown analysis file (default: results/inventory_management/Analysis_Report.md).",
            "1. Use the `Markdown to PDF Report Generator` tool.",
            "2. Provide the correct logo $logo_company.",
            "3. Save the generated PDF in results/inventory_management/report.pdf.",
            "4. Confirm the PDF path in the output."
            ]))