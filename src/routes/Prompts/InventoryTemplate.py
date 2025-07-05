from string import Template
from datetime import datetime



process_prompt =Template("\n".join([
                            f"Process the inventory data file: $full_data",
                            
                            "Your responsibilities:",
                            "1. Read and analyze the file structure",
                            "2. Validate data quality and identify any issues",
                            "3. Extract key information about inventory items",
                            "4. Prepare clean data summary for further analysis",
                            "5. Identify data patterns and basic statistics",
                            
                            "Provide a comprehensive data summary."
                            ]))


report_prompt =Template("\n".join([
                "A professional markdown report with the following structure:",
                "",
                "# Inventory Management Analysis Report",
                f"**Company:** $COMPANY_NAME",
                f"**Date:** {datetime.now().strftime('%Y-%m-%d, %H:%M')}",
                f"**INDUSTRY_NAME:** $INDUSTRY_NAME"
                "",
                "## 📊 Executive Summary",
                "- Key findings summary (200-300 words)",
                "- Critical business impacts",
                "- Priority recommendations",
                "",
                "## 🚨 Critical Alerts",
                "| Alert Type | Item | Severity | Impact | Action Required | Timeline |",
                "|------------|------|----------|--------|-----------------|----------|",
                "| .......... | .... | ........ | ...... | ............... | ........ |",
                "",
                "## 📈 Key Performance Indicators",
                "### Inventory Turnover",
                "| Category | Current | Target | Status | Trend |",
                "|----------|---------|--------|--------|-------|",
                "| ........ | ....... | ...... | ...... | ..... |",
                "",
                "### Service Levels",
                "| Metric | Current | Target | Gap | Action |",
                "|--------|---------|--------|-----|--------|",
                "| .......| ....... | ...... | ... | ...... |",
                "",
                "## 🔍 ABC Analysis",
                "### Classification Summary",
                "| Class | Items | Value % | Recommendations |",
                "|-------|-------|---------|-----------------|",
                "| A     |...... |........ | ................|",
                "| B     |...... |........ | ................|",
                "| C     |...... |........ | ................|",
                "",
                "## 🎯 Action Plan",
                "### Immediate Actions (0-48 hours)",
                "1. **Action 1:** Description, timeline, responsible party",
                "2. **Action 2:** Description, timeline, responsible party",
                "",
                "### Short-term Improvements (1-4 weeks)",
                "1. **Initiative 1:** Objective, resources needed, success metrics",
                "2. **Initiative 2:** Objective, resources needed, success metrics",
                "",
                "### Long-term Strategy (1-6 months)",
                "1. **Strategy 1:** Goals, ROI projection, implementation plan",
                "2. **Strategy 2:** Goals, ROI projection, implementation plan",
                "",
                "## 📋 Implementation Timeline",
                "| Phase | Duration | Key Milestones | Success Metrics |",
                "|-------|----------|----------------|-----------------|",
                "| ... ..| ........ | .............. | ............... |",
                "",
                f"**please use the Language:** $Language**for this report",
                "",
                "**Quality Requirements:**",
                "- Each section must be clearly separated with proper headers",
                "- All tables must be properly formatted with consistent columns",
                "- No raw CSV data presentation",
                "- Include specific, measurable recommendations",
                "- Use professional, executive-friendly language",
                "- NEVER output raw CSV data"
                "- ALWAYS convert to markdown tables",
                "- ALWAYS use | separators"
            ])

    
)


translation_prompt =Template("\n".join([
                        "Translate the comprehensive inventory analysis report from English to Arabic.",
                        "Ensure technical terms are accurately translated and the report maintains its professional structure and actionable insights."
                                        ]))