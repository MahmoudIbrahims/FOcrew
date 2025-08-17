import os
import re
import json
import logging
import pandas as pd
from typing import List, Type,Dict
from pydantic import BaseModel
from ydata_profiling import ProfileReport
from crewai.tools import BaseTool
from .Schema.MarkdownTableReaderSchema import MarkdownTableReaderSchema
import io


class MarkdownTableReader(BaseTool):
    name: str = "Markdown / Excel / CSV Reader"
    description: str = "Reads tables from Markdown, Excel, or CSV files, cleans them, and generates profiling reports."
    args_schema: Type[BaseModel] = MarkdownTableReaderSchema

    def _extract_tables_from_markdown(self, markdown_text: str) -> List[pd.DataFrame]:
        """Extract markdown tables from text and return as list of DataFrames."""
        tables = []
        table_regex = r"(\|.*\|\n\|[-:| ]+\|\n(?:\|.*\|\n?)*)"
        matches = re.findall(table_regex, markdown_text)

        for match in matches:
            try:
                cleaned_match = "\n".join(
                    [line.strip().strip("|") for line in match.strip().split("\n")]
                )
                df = pd.read_csv(io.StringIO(cleaned_match), sep="|")
                df = df.applymap(lambda x: str(x).strip() if pd.notna(x) else "")
                tables.append(df)
            except Exception as e:
                logging.warning(f"Error parsing table: {e}\nTable snippet:\n{match[:200]}")
        return tables

    def _clean_batch_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean DataFrame similar to JSON cleaning."""
        cleaned_df = df.copy()
        for col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].apply(lambda v:
                v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, pd.Timestamp) else
                "" if pd.isna(v) or v is None else
                v if isinstance(v, (int, float, str, bool)) else str(v)
            )
        return cleaned_df

    def _classify_table(self, df: pd.DataFrame) -> str:
        """Classify table type based on its columns."""
        cols = [c.lower().strip() for c in df.columns]
        if "metric" in cols and "value" in cols:
            return "metrics"
        elif "category" in cols and "count" in cols:
            return "categories"
        elif "internal reference" in cols or "product name" in cols:
            return "products"
        else:
            return "other"

    def _profile_and_save(self, df: pd.DataFrame, output_path: str, title: str):
        """Generate and save profiling report."""
        profile = ProfileReport(df, title=title, explorative=True)
        profile.to_file(output_path)
        logging.info(f"Profiling report saved to {output_path}")

    def _run(self, file_path: str, output_dir: str = "results/Dashboard") -> Dict[str, pd.DataFrame]:
        """Process Markdown, Excel, or CSV files and generate profiling reports."""
        try:
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            ext = os.path.splitext(file_path)[1].lower()

            # --- Case 1: Excel or CSV ---
            if ext in [".xlsx", ".xls", ".csv"]:
                logging.info(f"Reading structured file: {file_path}")
                if ext == ".csv":
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)

                output_html = os.path.join(output_dir, f"{base_name}_profile.html")
                self._profile_and_save(df, output_html, "Inventory Profiling Report")

                return {"combined": df}

            # --- Case 2: Markdown ---
            elif ext in [".md", ".markdown"]:
                logging.info(f"Reading Markdown file: {file_path}")
                with open(file_path, "r", encoding="utf-8") as f:
                    markdown_text = f.read()

                tables = self._extract_tables_from_markdown(markdown_text)
                logging.info(f"Found {len(tables)} tables in the markdown file.")

                cleaned_tables = [self._clean_batch_data(df) for df in tables]

                grouped_tables = {"metrics": [], "categories": [], "products": [], "other": []}
                for df in cleaned_tables:
                    group = self._classify_table(df)
                    grouped_tables[group].append(df)

                results = {}
                for group, dfs in grouped_tables.items():
                    if dfs:
                        merged_df = pd.concat(dfs, ignore_index=True)
                        results[group] = merged_df

                        output_html = os.path.join(output_dir, f"{base_name}_{group}_profile.html")
                        self._profile_and_save(merged_df, output_html, f"{group.capitalize()} Tables Profiling Report")

                # Combined report
                combined_list = []
                for group, df in results.items():
                    df = df.copy()
                    df["__table_type__"] = group
                    combined_list.append(df)

                if combined_list:
                    combined_df = pd.concat(combined_list, ignore_index=True)
                    results["combined"] = combined_df

                    combined_html = os.path.join(output_dir, f"{base_name}_combined_profile.html")
                    self._profile_and_save(combined_df, combined_html, "Combined Profiling Report (All Tables)")

                return results

            else:
                logging.error(f"Unsupported file format: {ext}")
                return {}

        except Exception as e:
            logging.error(f"Failed to process {file_path}: {str(e)}")
            return {}

    def read_file(self, file_path: str, output_dir: str = "results/Dashboard") -> Dict[str, pd.DataFrame]:
        """Direct method to read a file (Markdown, Excel, or CSV)."""
        return self._run(file_path, output_dir)
