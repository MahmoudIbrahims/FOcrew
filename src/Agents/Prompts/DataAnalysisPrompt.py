from string import Template

# Data_analysis_prompt = Template("\n".join([
#     "Analyze the uploaded dataset file: $file_path",
#     "",
#     "Use the tool `Live Jupyter Notebook (Web)` to show a live Python execution window (like Jupyter Notebook).",
#     "Use the `Live Jupyter Kernel Executor` tool to run each Python step.",
#     "",
#     "Steps:",
#     "1. Load the dataset using pandas.",
#     "2. Explore columns, data types, and missing values.",
#     "3. Clean the data if needed.",
#     "4. Generate summary statistics and visualizations.",
#     "5. Find trends or anomalies.",
#     "6. Combine all results into a final Markdown report.",
#     "",
#     "Save the final report to: results/inventory_management/Analysis_Report.md",
#     "",
# ]))





Data_analysis_prompt = Template("\n".join([
                "Analyze the uploaded dataset file: $file_path",
                "",
                "Use the tool `Live Jupyter Notebook (Web)` to run each Python step and visually display the results in the web interface.",
                "",
                "**Analysis and Execution Phases:**",
                "1. Load the dataset using pandas and display the head.",
                "2. Explore columns, data types, and missing values; then clean/preprocess the data as necessary.",
                "3. Generate summary statistics and **essential visualizations (using matplotlib/seaborn)** to understand key trends. (Note: The tool automatically captures and displays your graphs.)",
                "4. Identify key trends, anomalies, or actionable insights from the data and the generated charts.",
                "",
                "--- FINAL REPORTING PHASE (Executive Report) ---",
                
                "5. **Crucially:** After completing the analysis and visualization, conduct a comprehensive review of all executed code cells and their outputs.",
                "6. **Draft a professional Executive Report** intended for senior management.",
                "7. The report **MUST** be written in **clear, concise business language**, focusing heavily on **Business Insights** and **Actionable Recommendations** derived from your analysis.",
                "8. Use strong **Markdown** formatting (Headings, bolding, lists) to organize the report effectively.",
                "",
                "Save the final report to: results/inventory_management/Analysis_Report.md", # Assume you have a file saving tool available for the agent
                ""
]))

