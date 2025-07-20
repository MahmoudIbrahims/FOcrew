from string import Template
from datetime import datetime


Visualization_description_prompt =Template("\n".join([
    "You are provided with an inventory dataset located at the following file path:",
    "**File Path:** $file_path",
    "",
    "Your job is to:",
    "1. Create an interactive inventory dashboard and visual reports.",
    "2. Include charts, KPIs, and insights extracted from the data.",
    "3. Add interactive elements such as filters, hover tooltips, and drill-downs.",
    "4. 📁 Save the complete HTML dashboard to: 'results/Dashboard/Complete_Dashboard.html'.",
    "5. Confirm the dashboard is saved successfully before completing your task.",
    
]))


Visualization_expected_output_prompt = Template("\n".join([
    "# 📊 Interactive Inventory Dashboard – Visualization Output Summary",
    "",
    f"**Generated On:** {datetime.now().strftime('%Y-%m-%d, %H:%M')}",
    "**File Source:** $file_path",
    "**Prepared By:** Automated Data Visualization System",
    "**Visualization Objective:** Transform raw inventory data into actionable, interactive dashboards.",
    "",
    "## ✅ Output Deliverables",
    "- A complete interactive HTML dashboard has been generated.",
    "- The file includes charts, KPIs, and advanced filtering features.",
    "- Saved successfully to: `results/Dashboard/Complete_Dashboard.html`",
    "",]))