from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import pandas as pd
import os
import numpy as np
import json
from datetime import datetime

class InventoryInput(BaseModel):
    """Input schema for Inventory Analyzer Tool."""
    file_path: str = Field(..., description="Path to data file or data as JSON string")
    title: Optional[str] = Field("Inventory Data Analysis Report", description="Report title")
    output_path: Optional[str] = Field("results/inventory_management/DataAnalysis_Report.md", description="Output report path")

class InventoryAnalysisTool(BaseTool):
    name: str = "Inventory Data Analyzer"
    description: str = (
        "Analyzes any inventory dataset (Excel/CSV/JSON) without depending on specific column names. "
        "Detects column types, missing values, duplicates, numeric stats, category insights, time trends, "
        "expiry checks, and low-stock alerts."
    )
    args_schema: Type[BaseModel] = InventoryInput

    def _run(self, file_path: str, title: str = "Inventory Data Analysis Report",
             output_path: str = "results/inventory_management/DataAnalysis_Report.md") -> str:
        try:
            df = self._load_data(file_path)
            report = self._analyze_data(df, title, os.path.basename(file_path))
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            return f"Inventory analysis report saved to: {output_path}"
        except Exception as e:
            return f"Error analyzing data: {str(e)}"

    def _load_data(self, file_path: str) -> pd.DataFrame:
        if os.path.exists(file_path):
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path,encoding="utf-8")
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                return pd.read_excel(file_path,engine='openpyxl')
            else:
                raise ValueError("Unsupported file type.")
        else:
            try:
                data = json.loads(file_path)
                return pd.DataFrame(data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string or file path not found.")

    def _analyze_data(self, df: pd.DataFrame, title: str, filename: str) -> str:
        report = [f"# 📦 {title}\n", f"**File:** `{filename}`\n"]

        # Data Types
        report.append("\n## 🔍 Column Types:")
        for col in df.columns:
            report.append(f"- `{col}`: {df[col].dtype}")

        # Missing Values
        na = df.isna().sum()
        report.append("\n## ⚠️ Missing Values:")
        has_na = False
        for col, count in na.items():
            if count > 0:
                has_na = True
                report.append(f"- `{col}`: {count} missing")
        if not has_na:
            report.append("- No missing values")

        # Duplicates
        duplicates = df.duplicated().sum()
        report.append(f"\n## 📑 Duplicate Rows: {duplicates}")

        # Numeric Analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        report.append("\n## 📈 Numeric Summary:")
        for col in numeric_cols:
            stats = df[col].describe()
            report.append(f"- `{col}` → total: **{df[col].sum():,.2f}**, avg: {stats['mean']:.2f}, min: {stats['min']}, max: {stats['max']}, std: {stats['std']:.2f}")

        # Low stock / zero stock alerts
        qty_cols = [col for col in numeric_cols if any(x in col.lower() for x in ['qty', 'stock', 'balance'])]
        for col in qty_cols:
            low = df[df[col] < 10].shape[0]
            zero = df[df[col] == 0].shape[0]
            report.append(f"\n## 🧯 Stock Alerts in `{col}`:")
            report.append(f"- Zero stock: {zero}")
            report.append(f"- Low stock (<10): {low}")

        # Expiry detection
        date_cols = [col for col in df.columns if np.issubdtype(df[col].dtype, np.datetime64)]
        for col in date_cols:
            if 'exp' in col.lower() or 'expiry' in col.lower():
                expired = df[df[col] < datetime.now()].shape[0]
                report.append(f"\n## ☠️ Expired Products in `{col}`:")
                report.append(f"- Total expired: {expired}")

        # Categorical Insights
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            top_values = df[col].value_counts().head(5)
            report.append(f"\n## 🗃️ Top Categories in `{col}`:")
            for val, count in top_values.items():
                report.append(f"- `{val}`: {count}")

        report.append("\n---\n✅ Report generated without exposing raw row-level data.")
        return "\n".join(report)