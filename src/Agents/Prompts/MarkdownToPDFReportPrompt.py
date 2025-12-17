from string import Template

Convert_md_to_pdf_prompt =Template("\n".join([
            "Take the Markdown analysis file (default: results/Data_Analysis/Analysis_Report.md).",
            "1. Use the `Markdown to PDF Report Generator` tool.",
            "2. Provide the correct logo $logo_company.",
            "3. Save the generated PDF in $full_path.",
            "4. Confirm the PDF path in the output."
            ]))


