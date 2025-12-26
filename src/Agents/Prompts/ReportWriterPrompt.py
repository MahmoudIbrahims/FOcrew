from string import Template

report_writer_prompt =Template("\n".join([
            "Write a professional business-focused Markdown report summarizing all findings.\n\n"
                    "Steps:\n"
                    "The working directory is $working_dir.\n"
                    "1. Combine data summaries, analysis, and visual insights.\n"
                    "2. Write an executive-style report highlighting key insights, trends, and recommendations.\n"
                    "3. Save the report to $report_md_path using MarkdownTool."
                
            ]))
