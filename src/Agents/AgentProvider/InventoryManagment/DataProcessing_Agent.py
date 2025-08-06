from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.FileReading import BatchFileReader,JsonBatchFileReader,BatchProcessor
from ...Prompts.DataprocessingPrompt import Data_processingprompt
import os
import logging
from datetime import datetime,timedelta
from typing import List, Dict
import gc
import traceback
import shutil


# class DataProcessing(BaseAgent):
#     def __init__(self):
#         provider = ProviderLLM()
#         llm = provider.get_llm()
#         batch_file_reader = BatchFileReader()
#         Json_BatchFileReader = JsonBatchFileReader()

#         super().__init__(
#             name="Data Processing Specialist",
#             role="Data Processing Specialist",
#             goal="Process and analyze inventory data files efficiently regardless of size",
#             backstory="\n".join([
#                 "You are a data processing expert who specializes in handling various file formats and sizes.",
#                 "You can efficiently read, clean, and prepare inventory data for analysis, ensuring data quality and consistency."
#             ]),
#             llm=llm,
#             allow_delegation=False,
#             tools=[batch_file_reader, Json_BatchFileReader],
#         )

#         self.input_dir = "temp_batches/Breadfast.xlsx_1753569465.7975478_1031496/"
#         self.output_dir = "results/inventory_management/batch_reports/"
#         self.final_report_path = "results/inventory_management/data_analysis_report.md"

#         os.makedirs(self.output_dir, exist_ok=True)
#         os.makedirs(os.path.dirname(self.final_report_path), exist_ok=True)

#         self.all_data = []
#         self.batch_reports = []

#     def get_task(self):
#         return Task(
#             description="".join([
#                 "Process large inventory dataset in batches optimized for Gemini's context length. For each batch: ",
#                 "1. Analyze the batch to extract key insights. ",
#                 "2. Use only real data from the batch. ",
#                 "3. Save intermediate results per batch. ",
#                 "4. Combine into a final report. ",
#                 "5. save file in **results/inventory_management/data_analysis_report.md**"
#             ]),
#             agent=self.get_agent(),
#             expected_output='results/inventory_management/data_analysis_report.md'
#         )

#     def process_batches(self) -> None:
#         print(f"[INFO] Scanning input directory: {self.input_dir}")
#         batch_files = sorted([f for f in os.listdir(self.input_dir) if f.endswith('.json')])
#         print(f"[INFO] Found {len(batch_files)} batch files: {batch_files[:5]}...")

#         if not batch_files:
#             print("[ERROR] No JSON batch files found.")
#             return

#         for i, batch_file in enumerate(batch_files):
#             print(f"\n[INFO] Processing file {i+1}/{len(batch_files)}: {batch_file}")
#             try:
#                 batch_number = int(batch_file.replace('batch_', '').replace('.json', '')) + 1
#             except ValueError as ve:
#                 print(f"[WARNING] Invalid batch file name format: {batch_file}. Skipping... ({ve})")
#                 continue

#             batch_path = os.path.join(self.input_dir, batch_file)

#             # Step 1: Read batch file
#             try:
#                 batch_data = self.tools[1].read_file(batch_path)
#                 print(f"[INFO] Batch {batch_number} loaded successfully. Records: {len(batch_data)} | Type: {type(batch_data)}")
#                 if not batch_data:
#                     print(f"[WARNING] Batch {batch_number} is empty or invalid. Skipping...")
#                     continue
#             except Exception as e:
#                 print(f"[ERROR] Failed to read batch {batch_file}: {str(e)}")
#                 continue

#             # Step 2: Analyze batch
#             try:
#                 batch_insights = self.analyze_batch(batch_data, batch_number)
#                 if not batch_insights:
#                     print(f"[WARNING] No insights generated for batch {batch_number}")
#                     continue
#             except Exception as e:
#                 print(f"[ERROR] Failed to analyze batch {batch_number}: {str(e)}")
#                 continue

#             # Step 3: Save batch report
#             batch_report_path = os.path.join(self.output_dir, f"batch_{batch_number}_report.md")
#             try:
#                 os.makedirs(os.path.dirname(batch_report_path), exist_ok=True)
#                 self.save_batch_report(batch_insights, batch_report_path, batch_number)
#                 print(f"[INFO] Batch report saved to: {batch_report_path}")
#             except Exception as e:
#                 print(f"[ERROR] Failed to save batch report {batch_number}: {str(e)}")
#                 continue

#             # Step 4: Aggregate results
#             self.batch_reports.append({
#                 'batch_number': batch_number,
#                 'file': batch_file,
#                 'insights': batch_insights
#             })

#             self.all_data.extend(batch_data)
#             print(f"[INFO] Batch {batch_number} processed successfully.")

#             # Step 5: Cleanup
#             batch_data = None
#             batch_insights = None
#             gc.collect()

#         # Final report
#         try:
#             print(f"\n[INFO] Generating final report...")
#             self.generate_final_report()
#             print(f"[INFO] Final report saved at: {self.final_report_path}")
#         except Exception as e:
#             print(f"[ERROR] Failed to generate final report: {str(e)}")

#     def analyze_batch(self, batch_data: List[Dict], batch_number: int) -> Dict:
#         try:
#             insights = {
#                 'batch_number': batch_number,
#                 'total_items': len(batch_data),
#                 'unique_skus': set(),
#                 'product_ids': set(),
#                 'product_names': set(),
#                 'missing_data': {'skus': 0, 'product_ids': 0, 'product_names': 0, 'barcodes': 0},
#                 'financial_categories': {},
#                 'total_available_quantity': 0.0,
#                 'near_expiry_products': []
#             }

#             current_date = datetime.now()
#             for item in batch_data:
#                 sku = item.get('Product/Internal Reference')
#                 if sku:
#                     insights['unique_skus'].add(sku)
#                 else:
#                     insights['missing_data']['skus'] += 1

#                 product_id = item.get('Product/Internal Reference')
#                 if product_id:
#                     insights['product_ids'].add(product_id)
#                 else:
#                     insights['missing_data']['product_ids'] += 1

#                 product_name = item.get('Product/Name')
#                 if product_name:
#                     insights['product_names'].add(product_name)
#                 else:
#                     insights['missing_data']['product_names'] += 1

#                 barcode = item.get('Product/Barcode')
#                 if not barcode:
#                     insights['missing_data']['barcodes'] += 1

#                 category = item.get('Financial Category', 'Unknown')
#                 insights['financial_categories'][category] = insights['financial_categories'].get(category, 0) + 1

#                 quantity = item.get('Available Quantity', 0.0)
#                 insights['total_available_quantity'] += quantity

#                 expiry_date = item.get('Lot/Serial Number/Expiration Date')
#                 if expiry_date:
#                     try:
#                         expiry = datetime.strptime(expiry_date, '%Y-%m-%d %H:%M:%S')
#                         if expiry < current_date + timedelta(days=90):
#                             insights['near_expiry_products'].append({
#                                 'sku': sku,
#                                 'name': product_name,
#                                 'expiry_date': expiry_date
#                             })
#                     except ValueError:
#                         pass

#             insights['unique_skus_count'] = len(insights['unique_skus'])
#             insights['product_ids_count'] = len(insights['product_ids'])
#             insights['product_names_count'] = len(insights['product_names'])

#             insights['unique_skus'] = list(insights['unique_skus'])[:10]
#             insights['product_ids'] = list(insights['product_ids'])[:10]
#             insights['product_names'] = list(insights['product_names'])[:10]
#             insights['near_expiry_count'] = len(insights['near_expiry_products'])

#             return insights
#         except Exception as e:
#             print(f"[ERROR] Exception during analysis of batch {batch_number}: {str(e)}")
#             return {'batch_number': batch_number, 'error': str(e)}

#     def save_batch_report(self, insights: Dict, report_path: str, batch_number: int) -> None:
#         try:
#             with open(report_path, 'w', encoding='utf-8') as f:
#                 f.write(f"# Batch {batch_number} Analysis Report\n\n")
#                 f.write(f"**Total Items in Batch**: {insights.get('total_items', 0)}\n")
#                 f.write(f"**Unique SKUs**: {insights.get('unique_skus_count', 0)}\n")
#                 f.write(f"**Unique Product IDs**: {insights.get('product_ids_count', 0)}\n")
#                 f.write(f"**Unique Product Names**: {insights.get('product_names_count', 0)}\n")
#                 f.write(f"**Sample SKUs**: {', '.join(insights.get('unique_skus', []))}\n")
#                 f.write(f"**Sample Product IDs**: {', '.join(insights.get('product_ids', []))}\n")
#                 f.write(f"**Sample Product Names**: {', '.join(insights.get('product_names', []))}\n")
#                 f.write(f"\n### Missing Data\n")
#                 f.write(f"- SKUs missing: {insights['missing_data']['skus']}\n")
#                 f.write(f"- Product IDs missing: {insights['missing_data']['product_ids']}\n")
#                 f.write(f"- Product Names missing: {insights['missing_data']['product_names']}\n")
#                 if 'error' in insights:
#                     f.write(f"\n### Error\n{insights['error']}\n")
#         except Exception as e:
#             print(f"[ERROR] Failed to write batch report {report_path}: {str(e)}")

#     def generate_final_report(self) -> None:
#         try:
#             with open(self.final_report_path, 'w', encoding='utf-8') as f:
#                 f.write("# Final Inventory Data Analysis Report\n\n")
#                 f.write(f"**Total Batches Processed**: {len(self.batch_reports)}\n")
#                 f.write(f"**Total Items Processed**: {len(self.all_data)}\n\n")

#                 all_skus = set()
#                 all_product_ids = set()
#                 all_product_names = set()
#                 total_missing = {'skus': 0, 'product_ids': 0, 'product_names': 0}

#                 for report in self.batch_reports:
#                     insights = report['insights']
#                     all_skus.update(insights.get('unique_skus', []))
#                     all_product_ids.update(insights.get('product_ids', []))
#                     all_product_names.update(insights.get('product_names', []))
#                     for key in total_missing:
#                         total_missing[key] += insights['missing_data'][key]

#                 f.write("## Aggregated Insights\n")
#                 f.write(f"- **Total Unique SKUs**: {len(all_skus)}\n")
#                 f.write(f"- **Total Unique Product IDs**: {len(all_product_ids)}\n")
#                 f.write(f"- **Total Unique Product Names**: {len(all_product_names)}\n")
#                 f.write(f"- **Sample SKUs**: {', '.join(list(all_skus)[:10])}\n")
#                 f.write(f"- **Sample Product IDs**: {', '.join(list(all_product_ids)[:10])}\n")
#                 f.write(f"- **Sample Product Names**: {', '.join(list(all_product_names)[:10])}\n")
#                 f.write("\n## Missing Data Summary\n")
#                 f.write(f"- SKUs missing: {total_missing['skus']}\n")
#                 f.write(f"- Product IDs missing: {total_missing['product_ids']}\n")
#                 f.write(f"- Product Names missing: {total_missing['product_names']}\n")

#                 f.write("\n## Batch Summaries\n")
#                 for report in self.batch_reports:
#                     insights = report['insights']
#                     f.write(f"### Batch {report['batch_number']} ({report['file']})\n")
#                     f.write(f"- Total Items: {insights.get('total_items', 0)}\n")
#                     f.write(f"- Unique SKUs: {insights.get('unique_skus_count', 0)}\n")
#                     f.write(f"- Unique Product IDs: {insights.get('product_ids_count', 0)}\n")
#                     f.write(f"- Unique Product Names: {insights.get('product_names_count', 0)}\n")
#                     if 'error' in insights:
#                         f.write(f"- Error: {insights['error']}\n")
#         except Exception as e:
#             print(f"[ERROR] Failed to write final report: {str(e)}")

#     def execute(self) -> None:
#         task = self.get_task()
#         print("[INFO] Starting batch processing task...")
#         self.process_batches()
#         print("[INFO] All batch processing completed.")


#=================================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_processing.log'),
        logging.StreamHandler()
    ]
)

class DataProcessing(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        batch_file_reader = BatchFileReader()
        Json_BatchFileReader = JsonBatchFileReader()
        Batch_Processor =BatchProcessor()

        super().__init__(
            name="Data Processing Specialist",
            role="Data Processing Specialist",
            goal="Process and analyze inventory data files efficiently regardless of size",
            backstory="\n".join([
                "You are a data processing expert who specializes in handling various file formats and sizes.",
                "You can efficiently read, clean, and prepare inventory data for analysis, ensuring data quality and consistency."
            ]),
            llm=llm,
            allow_delegation=False,
            tools=[batch_file_reader, Json_BatchFileReader,Batch_Processor],
        )
        

    def get_task(self):
        return Task(
            description="".join([
                "Process large inventory dataset in batches optimized for Gemini's context length. For each batch: ",
                "1. Use the 'Batch Processor' tool to process ALL ",
                "2. Use only real data from the batch. ",
                "3. Save intermediate results per batch. ",
                "4. Combine into a final report. ",
                "5. save file in **results/inventory_management/data_analysis_report.md**"
            ]),
            agent=self.get_agent(),
            expected_output='results/inventory_management/data_analysis_report.md'
        )
