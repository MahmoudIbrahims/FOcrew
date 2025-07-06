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
    "# 📊 Executive Inventory Strategy Report – Full Advisory Format",
    "",
    "**Client:** $COMPANY_NAME",
    "**Industry:** $INDUSTRY_NAME",
    f"**Date:** {datetime.now().strftime('%Y-%m-%d, %H:%M')}",
    "**Prepared By:** Senior Inventory Optimization Consultant",
    "**Language:** $Language — Please write all report content, labels, and descriptions in this language.",
    "",
    "> ⚠️ Note: Ensure each analytical table includes **at least 10 products/items**, sorted by priority or impact (from most critical to least). Prioritize items based on expiry risk, financial exposure, turnover rate, or classification weight.",
    "",
    "## 🔷 Executive Summary",
    "- Provide a strategic overview with maximum insight and minimum fluff (250–300 words).",
    "- Identify key inventory inefficiencies, risks, and value leaks.",
    "- Align findings with global best practices (SCOR, APICS, Lean, DDMRP).",
    "",
    "## 🚨 High-Risk & Strategic Exposure Items",
    "| Risk Type | SKU | Root Cause | Severity | Financial Impact | Strategic Action |",
    "|-----------|-----|------------|----------|------------------|------------------|",
    "| (Top 10 risks – sorted from highest exposure to lowest) |",
    "",
    "## ⌛ Expiry Risk Report – Shelf-Life Critical Items",
    "### ⚠️ Items Expiring Within Next 60 Days",
    "| SKU | Product Name | Expiry Date | Qty | Days Remaining | Priority Level | Recommended Action |",
    "|-----|--------------|-------------|-----|----------------|----------------|---------------------|",
    "| (Include 10 products, sorted by earliest expiry & highest volume) |",
    "",
    "### ❌ Already Expired Inventory",
    "| SKU | Product Name | Expired On | Qty | Financial Value | Treatment Plan |",
    "|-----|--------------|------------|-----|-----------------|----------------|",
    "| (Include top 10 expired items by cost or quantity) |",
    "",
    "## 📈 KPI Dashboard – Key Inventory Metrics",
    "| KPI | Current | Target | Gap | Impact Level | Action Required |",
    "|-----|---------|--------|-----|---------------|------------------|",
    "- Include actionable KPIs (e.g., Turnover, Fill Rate, Carrying Cost).",
    "",
    "## 🔍 ABC Inventory Analysis – Top Value SKUs",
    "### Top 10 High-Value 'A' Class Items",
    "| SKU | Product Name | Inventory Value | % of Total | Monthly Movement | Recommendation |",
    "|-----|--------------|-----------------|-------------|------------------|----------------|",
    "",
    "## 🔁 XYZ Analysis – Demand Variability (Top 10)",
    "| SKU | Demand Pattern (X/Y/Z) | Std Dev | Sales Consistency | Category | Action |",
    "|-----|------------------------|---------|-------------------|----------|--------|",
    "",
    "## 💰 Financial Impact Breakdown",
    "- Total capital tied in excess stock: $___",
    "- Estimated stockout loss: $___",
    "- Expired stock loss: $___",
    "- Working capital recovery potential: $___",
    "",
    "## 🎯 Strategic Roadmap",
    "### Phase 1 – Immediate (0–7 days)",
    "- Restock top 10 most-critical SKUs.",
    "- Quarantine & document expired inventory.",
    "",
    "### Phase 2 – Short-Term (1–6 weeks)",
    "- Implement FEFO (First-Expire-First-Out) logic for top 10 at-risk SKUs.",
    "- Adjust min/max stock levels based on ABC-XYZ matrix.",
    "",
    "### Phase 3 – Long-Term (2–6 months)",
    "- Integrate expiry tracking in inventory software.",
    "- Adopt predictive analytics for demand & expiry risk.",
    "",
    "## 📋 Execution Timeline",
    "| Task | Owner | Due Date | Milestone | Success Metric |",
    "|------|--------|----------|-----------|----------------|",
    "",
    "**Important Reporting Guidelines:**",
    "- All tables should have **10 items at minimum**, sorted by impact or priority.",
    "- Do not output raw data — only professional insights.",
    "- Format all tables using markdown with `|` separators.",
    "- Maintain consulting-level tone throughout the report.",
    "- Use real-world business vocabulary and focus on executive action."
]))


translation_prompt =Template("\n".join([
                        "Translate the comprehensive inventory analysis report from English to Arabic.",
                        "Ensure technical terms are accurately translated and the report maintains its professional structure and actionable insights."
                                        ]))