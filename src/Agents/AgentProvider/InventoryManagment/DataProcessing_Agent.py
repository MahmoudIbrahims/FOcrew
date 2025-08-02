from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.FileReading import FileTool,DirectoryTool,BatchFileReader
import json
import os
import logging


# class DataProcessing(BaseAgent):
#     def __init__(self):
#         provider = ProviderLLM()
#         llm = provider.get_llm()
#         file_tool = FileTool()
#         directory_tool =DirectoryTool()
#         batch_file_reader =BatchFileReader()
#         super().__init__(
#                     name="Data Processing Specialist",
#                     role="Data Processing Specialist",
#                     goal="Process and analyze inventory data files efficiently regardless of size",
#                     backstory="\n".join([
#                         "You are a data processing expert who specializes in handling various file formats and sizes."
#                         "You can efficiently read, clean, and prepare inventory data for analysis, ensuring data quality and consistency."
#                         ]),
#                     llm=llm,
#                     allow_delegation=False,
#                     tools=[batch_file_reader], 
#                     # reasoning=True,  # Enable reasoning
#                     # max_reasoning_attempts=5  # Optional: Set a maximum number of reasoning attempts
#                     )
            
                     
#     def get_task(self):
#         return Task(
#             description="".join([
#                "Analyze the inventory dataset and generate a strategic report based on real data only. ",
#                 "🚨 You MUST use the exact SKUs, Product IDs, and Product Names from the original uploaded file. ",
#                 "Never fabricate, infer, rename, or guess any values. Ensure the report reflects actual data integrity. ",
#                 "📁 IMPORTANT: Save your final analysis report to 'results/inventory_management/data_analysis_report.md'. ",
#                 "Create the directory structure if it doesn't exist and write the complete analysis to the file."
#             ]),
            
#             agent=self.get_agent(),
#             expected_output="A comprehensive data analysis report saved to results/inventory_management/data_analysis_report.md"
#         )
#======================================================

# class DataProcessing(BaseAgent):
#     def __init__(self):
#         provider = ProviderLLM()  # Assuming this returns Gemini LLM
#         llm = provider.get_llm()
#         batch_file_reader = BatchFileReader()
#         super().__init__(
#             name="Data Processing Specialist",
#             role="Data Processing Specialist",
#             goal="Process and analyze large inventory data files efficiently with Gemini",
#             backstory="\n".join([
#                 "You are a data processing expert specializing in handling large datasets in various formats.",
#                 "You ensure data quality and consistency, processing data in batches to fit within Gemini's context length."
#             ]),
#             llm=llm,
#             allow_delegation=False,
#             tools=[batch_file_reader],
#         )

#     def get_task(self):
#         return Task(
#             description="".join([
#                 "Process large inventory dataset in batches optimized for Gemini's context length. For each batch: ",
#                 "1. Analyze the batch to extract key insights (e.g., SKUs, Product IDs, Product Names). ",
#                 "2. Use only real data from the batch; do not fabricate or guess any values. ",
#                 "3. Save intermediate results for each batch to 'results/inventory_management/batch_{i}_report.md'. ",
#                 "4. After processing all batches, combine insights into a final strategic report. ",
#                 "5. Save the final report to 'results/inventory_management/data_analysis_report.md'. ",
#                 "Create the directory structure if it doesn't exist."
#             ]),
#             agent=self.get_agent(),
#             expected_output="A comprehensive data analysis report saved to results/inventory_management/data_analysis_report.md, with intermediate batch reports."
#         )  

#=============================================


# # Set up logging
# logging.basicConfig(filename='data_processing.log', level=logging.DEBUG, 
#                     format='%(asctime)s %(levelname)s: %(message)s')

# class DataProcessing(BaseAgent):
#     def __init__(self):
#         provider = ProviderLLM()
#         llm = provider.get_llm()
#         batch_file_reader = BatchFileReader()
#         super().__init__(
#             name="Data Processing Specialist",
#             role="Data Processing Specialist",
#             goal="Process and analyze large inventory data files efficiently with Gemini",
#             backstory="\n".join([
#                 "You are a data processing expert specializing in handling large datasets in various formats.",
#                 "You process data in small batches from temporary JSON files to fit within Gemini's context length."
#             ]),
#             llm=llm,
#             allow_delegation=False,
#             tools=[batch_file_reader],
#         )

#     def _analyze_batch(self, batch_data):
#         """Analyze a batch and extract key insights."""
#         try:
#             num_records = len(batch_data)
#             skus = [record.get("Product/Internal Reference", "") for record in batch_data]
#             names = [record.get("Product/Name", "") for record in batch_data]
#             categories = set(record.get("Financial Category", "") for record in batch_data)
#             locations = set(record.get("Location", "") for record in batch_data)
#             quantities = [record.get("Available Quantity", 0) for record in batch_data]
#             missing_dates = sum(1 for record in batch_data if not record.get("Lot/Serial Number/Production Date", ""))

#             return f"""
# Batch Analysis:
# - Number of records: {num_records}
# - Unique SKUs: {len(set(skus))}
# - Product Names: {', '.join(set(names)[:5])} (showing up to 5)
# - Categories: {', '.join(categories)}
# - Locations: {', '.join(locations)}
# - Average Available Quantity: {(sum(quantities) / num_records if num_records > 0 else 0):.2f}
# - Records with missing dates: {missing_dates}
# """
#         except Exception as e:
#             logging.error(f"Error analyzing batch: {str(e)}")
#             return f"Error analyzing batch: {str(e)}"

#     def get_task(self):
#         return Task(
#             description="".join([
#                 "Process large inventory dataset from batch JSON files. For each batch file: ",
#                 "1. Read the batch data from the provided JSON file path. ",
#                 "2. Analyze the batch to extract key insights (e.g., SKUs, Product Names, Categories, Locations, Quantities). ",
#                 "3. Use only real data from the batch; do not fabricate or guess any values. ",
#                 "4. Save intermediate results for each batch to 'results/inventory_management/batch_{i}_report.md'. ",
#                 "5. After processing all batches, combine insights into a final strategic report. ",
#                 "6. Save the final report to 'results/inventory_management/data_analysis_report.md'. ",
#                 "7. Create the directory structure if it doesn't exist. ",
#                 "8. Process one batch at a time to avoid overwhelming Gemini's context length. ",
#                 "9. If a batch file is corrupted or empty, skip it and log the issue."
#             ]),
#             agent=self.get_agent(),
#             expected_output="results/inventory_management/data_analysis_report.md",
#             callback=self._process_batch_callback
#         )

#     def _process_batch_callback(self, result):
#         """Callback to process each batch file and generate reports."""
#         try:
#             batch_files = result
#             os.makedirs("results/inventory_management", exist_ok=True)
#             all_insights = []
#             data_structure = None
#             missing_values = {"total_records": 0, "missing_dates": 0}
#             unique_products = set()
#             quantities = []
#             categories = set()
#             locations = set()

#             for i, batch_file in enumerate(batch_files):
#                 try:
#                     logging.info(f"Processing batch file: {batch_file}")
#                     with open(batch_file, "r", encoding="utf-8") as f:
#                         batch_data = json.load(f)
#                     insights = self._analyze_batch(batch_data)
#                     with open(f"results/inventory_management/batch_{i}_report.md", "w", encoding="utf-8") as f:
#                         f.write(f"# Batch {i} Analysis\n\n{insights}")
#                     all_insights.append(insights)

#                     # Aggregate statistics
#                     if not data_structure and batch_data:
#                         data_structure = {key: str(type(value)) for key, value in batch_data[0].items()}
#                     missing_values["total_records"] += len(batch_data)
#                     missing_values["missing_dates"] += sum(1 for record in batch_data if not record.get("Lot/Serial Number/Production Date", ""))
#                     unique_products.update(record.get("Product/Internal Reference", "") for record in batch_data)
#                     quantities.extend(record.get("Available Quantity", 0) for record in batch_data)
#                     categories.update(record.get("Financial Category", "").split(" / ") for record in batch_data)
#                     locations.update(record.get("Location", "") for record in batch_data)
#                     logging.info(f"Processed batch {i} successfully")
#                 except Exception as e:
#                     logging.error(f"Error processing batch {i} from {batch_file}: {str(e)}")
#                     continue

#             # Generate final report
#             final_report = "# Final Inventory Analysis Report\n\n"
#             final_report += "## 1. Introduction\n"
#             final_report += "- Purpose: Analyze inventory data from Breadfast.xlsx.\n"
#             final_report += "- Data Source: Breadfast.xlsx\n\n"
            
#             final_report += "## 2. Data Structure\n"
#             final_report += f"- Columns and Types: {json.dumps(data_structure, indent=2) if data_structure else 'Not available'}\n\n"
            
#             final_report += "## 3. Data Quality Assessment\n"
#             final_report += f"- Total Records: {missing_values['total_records']}\n"
#             final_report += f"- Missing Dates: {missing_values['missing_dates']} ({(missing_values['missing_dates'] / missing_values['total_records'] * 100):.2f}%)\n"
#             final_report += "- Inconsistent Data: Not fully analyzed due to incomplete processing\n\n"
            
#             final_report += "## 4. Key Inventory Information\n"
#             final_report += f"- Unique Products: {len(unique_products)}\n"
#             final_report += f"- Total Quantities: {sum(quantities) if quantities else 0}\n"
#             final_report += f"- Categories: {', '.join(categories)}\n"
#             final_report += f"- Locations: {', '.join(locations)}\n\n"
            
#             final_report += "## 5. Data Patterns and Statistics\n"
#             final_report += f"- Average Quantity: {(sum(quantities) / len(quantities) if quantities else 0):.2f}\n"
#             final_report += f"- Median Quantity: {(sorted(quantities)[len(quantities)//2] if quantities else 0):.2f}\n"
#             final_report += "- Trends: Not fully analyzed due to incomplete processing\n\n"
            
#             final_report += "## 6. Batch Reports\n"
#             final_report += "\n".join(all_insights)
            
#             final_report += "## 7. Conclusion\n"
#             final_report += "- Summary: Partial analysis completed due to processing limitations.\n"
#             final_report += "- Recommendations: Optimize batch sizes and ensure LLM stability.\n"

#             with open("results/inventory_management/data_analysis_report.md", "w", encoding="utf-8") as f:
#                 f.write(final_report)
#             logging.info("Final report generated")
#             return final_report
#         except Exception as e:
#             logging.error(f"Error in callback: {str(e)}")
#             return f"Error in processing batches: {str(e)}"   

#===============================================

# # Set up logging
# logging.basicConfig(filename='data_processing.log', level=logging.DEBUG, 
#                     format='%(asctime)s %(levelname)s: %(message)s')

# class DataProcessing(BaseAgent):
#     def __init__(self):
#         provider = ProviderLLM()
#         llm = provider.get_llm()
#         batch_file_reader = BatchFileReader()
#         super().__init__(
#             name="Data Processing Specialist",
#             role="Data Processing Specialist",
#             goal="Process and analyze large inventory data files efficiently with Gemini",
#             backstory="\n".join([
#                 "You are a data processing expert specializing in handling large datasets in various formats.",
#                 "You process data in small batches from temporary JSON files to fit within Gemini's context length."
#             ]),
#             llm=llm,
#             allow_delegation=False,
#             tools=[batch_file_reader],
#         )

#     def _analyze_batch(self, batch_data):
#         """Analyze a batch and extract key insights."""
#         try:
#             num_records = len(batch_data)
#             skus = [record.get("Product/Internal Reference", "") for record in batch_data]
#             names = [record.get("Product/Name", "") for record in batch_data]
#             categories = set(record.get("Financial Category", "") for record in batch_data)
#             locations = set(record.get("Location", "") for record in batch_data)
#             quantities = [float(record.get("Available Quantity", 0)) for record in batch_data]
#             quantities_total = [float(record.get("Quantity", 0)) for record in batch_data]
#             missing_dates = sum(1 for record in batch_data if not record.get("Lot/Serial Number/Production Date", "") or not record.get("Lot/Serial Number/Expiration Date", ""))
            
#             return f"""
# Batch Analysis:
# - Number of records: {num_records}
# - Unique SKUs: {len(set(skus))}
# - Product Names: {', '.join(set(names)[:5])} (showing up to 5)
# - Categories: {', '.join(categories)}
# - Locations: {', '.join(locations)}
# - Average Available Quantity: {(sum(quantities) / num_records if num_records > 0 else 0):.2f}
# - Average Total Quantity: {(sum(quantities_total) / num_records if num_records > 0 else 0):.2f}
# - Records with missing dates: {missing_dates}
# """
#         except Exception as e:
#             logging.error(f"Error analyzing batch: {str(e)}")
#             return f"Error analyzing batch: {str(e)}"

#     def get_task(self):
#         return Task(
#             description="".join([
#                 "Process large inventory dataset from batch JSON files. For each batch file: ",
#                 "1. Read the batch data from the provided JSON file path. ",
#                 "2. Analyze the batch to extract key insights (e.g., Product/Internal Reference, Product/Name, Financial Category, Locations, Available Quantity ,Quantity). ",
#                 "3. Use only real data from the batch; do not fabricate or guess any values. ",
#                 "4. Save intermediate results for each batch to 'results/inventory_management/batch_{i}_report.md'. ",
#                 "5. After processing all batches, combine insights into a final strategic report. ",
#                 "6. Save the final report to 'results/inventory_management/data_analysis_report.md'. ",
#                 "7. Create the directory structure if it doesn't exist. ",
#                 "8. Process one batch at a time to avoid overwhelming Gemini's context length. ",
#                 "9. If a batch file is corrupted or empty, skip it and log the issue."
#             ]),
#             agent=self.get_agent(),
#             expected_output="A comprehensive data analysis report saved to results/inventory_management/data_analysis_report.md, with intermediate batch reports.",
#             callback=self._process_batch_callback
#         )

#     def _process_batch_callback(self, result):
#         """Callback to process each batch file and generate reports."""
#         try:
#             # Ensure result is a list of file paths
#             if not isinstance(result, list) or not all(isinstance(f, str) for f in result):
#                 logging.error(f"Invalid batch files format: {result}")
#                 raise ValueError(f"Expected list of file paths, got: {result}")

#             batch_files = result
#             os.makedirs("results/inventory_management", exist_ok=True)
#             all_insights = []
#             data_structure = None
#             missing_values = {"total_records": 0, "missing_dates": 0}
#             unique_products = set()
#             quantities = []
#             quantities_total = []
#             categories = set()
#             locations = set()

#             for i, batch_file in enumerate(batch_files):
#                 try:
#                     # Check if batch file exists
#                     if not os.path.exists(batch_file):
#                         logging.error(f"Batch file {batch_file} does not exist")
#                         continue

#                     logging.info(f"Processing batch file: {batch_file}")
#                     with open(batch_file, "r", encoding="utf-8") as f:
#                         batch_data = json.load(f)
                    
#                     # Check if batch_data is empty
#                     if not batch_data:
#                         logging.warning(f"Batch file {batch_file} is empty")
#                         continue

#                     insights = self._analyze_batch(batch_data)
#                     batch_report_path = f"results/inventory_management/batch_{i}_report.md"
#                     with open(batch_report_path, "w", encoding="utf-8") as f:
#                         f.write(f"# Batch {i} Analysis\n\n{insights}")
#                     logging.info(f"Saved batch report to {batch_report_path}")
#                     all_insights.append(insights)

#                     # Aggregate statistics
#                     if not data_structure and batch_data:
#                         data_structure = {key: str(type(value)) for key, value in batch_data[0].items()}
#                     missing_values["total_records"] += len(batch_data)
#                     missing_values["missing_dates"] += sum(1 for record in batch_data if not record.get("Lot/Serial Number/Production Date", "") or not record.get("Lot/Serial Number/Expiration Date", ""))
#                     unique_products.update(record.get("Product/Internal Reference", "") for record in batch_data)
#                     quantities.extend(float(record.get("Available Quantity", 0)) for record in batch_data)
#                     quantities_total.extend(float(record.get("Quantity", 0)) for record in batch_data)
#                     categories.update(record.get("Financial Category", "") for record in batch_data)
#                     locations.update(record.get("Location", "") for record in batch_data)
#                     logging.info(f"Processed batch {i} successfully")
#                 except Exception as e:
#                     logging.error(f"Error processing batch {i} from {batch_file}: {str(e)}")
#                     continue

#             # Generate final report
#             final_report = "# Final Inventory Analysis Report\n\n"
#             final_report += "## 1. Introduction\n"
#             final_report += "- Purpose: Analyze inventory data from Breadfast.xlsx.\n"
#             final_report += "- Data Source: Breadfast.xlsx\n\n"
            
#             final_report += "## 2. Data Structure\n"
#             final_report += f"- Columns and Types: {json.dumps(data_structure, indent=2) if data_structure else 'Not available'}\n\n"
            
#             final_report += "## 3. Data Quality Assessment\n"
#             final_report += f"- Total Records: {missing_values['total_records']}\n"
#             final_report += f"- Missing Dates: {missing_values['missing_dates']} ({(missing_values['missing_dates'] / missing_values['total_records'] * 100):.2f}%)\n"
#             final_report += "- Inconsistent Data: Not fully analyzed due to incomplete processing\n\n"
            
#             final_report += "## 4. Key Inventory Information\n"
#             final_report += f"- Unique Products: {len(unique_products)}\n"
#             final_report += f"- Total Available Quantity: {sum(quantities) if quantities else 0:.2f}\n"
#             final_report += f"- Total Quantity: {sum(quantities_total) if quantities_total else 0:.2f}\n"
#             final_report += f"- Categories: {', '.join(categories)}\n"
#             final_report += f"- Locations: {', '.join(locations)}\n\n"
            
#             final_report += "## 5. Data Patterns and Statistics\n"
#             final_report += f"- Average Available Quantity: {(sum(quantities) / len(quantities) if quantities else 0):.2f}\n"
#             final_report += f"- Median Available Quantity: {(sorted(quantities)[len(quantities)//2] if quantities else 0):.2f}\n"
#             final_report += f"- Average Total Quantity: {(sum(quantities_total) / len(quantities_total) if quantities_total else 0):.2f}\n"
#             final_report += "- Trends: Not fully analyzed due to incomplete processing\n\n"
            
#             final_report += "## 6. Batch Reports\n"
#             final_report += "\n".join(all_insights)
            
#             final_report += "## 7. Conclusion\n"
#             final_report += "- Summary: Partial analysis completed due to processing limitations.\n"
#             final_report += "- Recommendations: Optimize batch sizes, ensure stable LLM processing, and validate data consistency.\n"

#             final_report_path = "results/inventory_management/data_analysis_report.md"
#             with open(final_report_path, "w", encoding="utf-8") as f:
#                 f.write(final_report)
#             logging.info(f"Final report saved to {final_report_path}")
#             return final_report
#         except Exception as e:
#             logging.error(f"Error in callback: {str(e)}")
#             return f"Error in processing batches: {str(e)}"   


# #=====================================================


