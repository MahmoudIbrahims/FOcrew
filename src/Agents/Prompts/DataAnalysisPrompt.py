from string import Template

Data_analysis_prompt = Template("\n".join([
    "Analyze the uploaded dataset file: $file_path",
    "",
    "Use the tool `Live Jupyter Notebook (Web)` to show a live Python execution window (like Jupyter Notebook).",
    "Use the `Live Jupyter Kernel Executor` tool to run each Python step.",
    "",
    "Steps:",
    "1. Load the dataset using pandas.",
    "2. Explore columns, data types, and missing values.",
    "3. Clean the data if needed.",
    "4. Generate summary statistics and visualizations.",
    "5. Find trends or anomalies.",
    "6. Combine all results into a final Markdown report.",
    "",
    "Save the final report to: results/inventory_management/Analysis_Report.md",
    "",
]))


