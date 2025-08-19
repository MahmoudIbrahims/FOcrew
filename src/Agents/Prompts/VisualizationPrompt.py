from string import Template


Visualization_Prompt =Template("\n".join([
            f"Process the inventory data file:$file_path",  
            "1. Use the `MarkdownTableReader` tool to read and clean all data from the file. ",
            "2. Generate a profiling HTML report from dataset ",
            "3. Save the profiling report in the same directory as the markdown file with `_profile.html` suffix. ",
            "## finally save the report HTML in **'results/Dashboard/Profiling_Report.html'**"
                
                                            ]))