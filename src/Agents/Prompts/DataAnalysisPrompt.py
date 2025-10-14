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



# Data_analysis_prompt = Template("\n".join([

#                 "You have been provided with a dataset file located at: `$file_path`.",
#                 "",
#                 "🎯 **Your mission:**",
#                 "1. Load and inspect the dataset using Python (pandas).",
#                 "2. Analyze structure (columns, nulls, data types).",
#                 "3. Perform exploratory data analysis (EDA).",
#                 "4. Create visualizations (if relevant).",
#                 "5. Identify issues or anomalies and describe insights.",
#                 "",
#                 "---",
#                 "🧠 **Error Handling Protocol:**",
#                 "- If any error occurs while running code in the Jupyter tool:",
#                 "  * Read and interpret the traceback carefully.",
#                 "  * Diagnose the exact cause (e.g., missing column, NaN issue, wrong variable name, plotting error).",
#                 "  * Correct the code step-by-step.",
#                 "  * Re-run the corrected version automatically until successful.",
#                 "  * Document the correction you made (what failed, why, and how you fixed it).",
#                 "",
#                 "---",
#                 "💡 **Tools to Use:**",
#                 "* Use `Live Jupyter Notebook (Web)` to display your live notebook interface.",
#                 "* Use `Live Jupyter Kernel Executor` to execute your Python code and visualize results.",
#                 "",
#                 "---",
#                 "📦 **Final Deliverable:**",
#                 "Generate a well-formatted markdown analysis report containing:",
#                 "- Dataset summary and key metrics",
#                 "- Data issues or inconsistencies",
#                 "- Graphs and descriptive statistics",
#                 "- Insights and business recommendations",
#                 "",
#                 "Save your final report to: `results/inventory_management/Analysis_Report.md`"


# ]))