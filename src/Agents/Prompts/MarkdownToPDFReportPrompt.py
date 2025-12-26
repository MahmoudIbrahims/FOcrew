from string import Template

Convert_md_to_pdf_prompt =Template("\n".join([
            "The working directory is $working_dir.\n"
            "Take the Markdown analysis file from $file_path.\n"
            "1. Use the `Markdown to PDF Report Generator` tool.\n"
            "2. Save the generated PDF in $output_report.\n"
            "3. Confirm the PDF path in the output.\n"
            ]))


