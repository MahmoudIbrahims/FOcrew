from crewai_tools import FileReadTool,DirectoryReadTool
from .Schema import BatchFileReaderSchema,JsonBatchFileReaderSchema
from crewai.tools import BaseTool
from pydantic import BaseModel
import dask.dataframe as dd
from typing import Type,List
import pandas as pd
import time
import json
import os
import logging


logging.basicConfig(filename='batch_reader.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_processing.log'),
        logging.StreamHandler()
    ]
)

#===============================================
def FileTool():
    file_tool = FileReadTool()
    return file_tool

#=================================================
    
def DirectoryTool():
    directory_tool = DirectoryReadTool()
    return directory_tool

#=================================================

class BatchFileReader(BaseTool):
    name: str = "Optimized Batch File Reader"
    description: str = "Reads CSV or Excel files in batches optimized for Gemini's context length with caching."
    args_schema: Type[BaseModel] = BatchFileReaderSchema
    
    def _get_cache_key(self, file_path: str) -> str:
        """Create cache key for files"""
        try:
            stat = os.stat(file_path)
            return f"{os.path.basename(file_path)}_{stat.st_mtime}_{stat.st_size}"
        except:
            return f"{os.path.basename(file_path)}_no_stat"
    
    def _check_existing_batches(self, cache_key: str) -> list:
        """check existing"""
        cache_dir = f"temp_batches/{cache_key}"
        if not os.path.exists(cache_dir):
            return []
        
        batch_files = []
        batch_index = 0
        while True:
            batch_file = f"{cache_dir}/batch_{batch_index}.json"
            if os.path.exists(batch_file):
                batch_files.append(batch_file)
                batch_index += 1
            else:
                break
        
        if batch_files:
            logging.info(f"Found {len(batch_files)} existing batch files")
        
        return batch_files
    
    def _clean_batch_data(self, batch_data: list) -> list:
        """Convert Timestamp objects and non-serializable types to strings."""
        cleaned_data = []
        for record in batch_data:
            if not isinstance(record, dict):
                continue
                
            cleaned_record = {}
            for key, value in record.items():
                try:
                    if isinstance(value, pd.Timestamp):
                        cleaned_record[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                    elif pd.isna(value):
                        cleaned_record[key] = ""
                    elif isinstance(value, (int, float, str, bool)):
                        cleaned_record[key] = value
                    elif value is None:
                        cleaned_record[key] = ""
                    else:
                        cleaned_record[key] = str(value)
                except Exception as e:
                    logging.warning(f"Error cleaning field {key}: {str(e)}")
                    cleaned_record[key] = ""
            
            cleaned_data.append(cleaned_record)
        return cleaned_data
    
    def _estimate_tokens(self, data: list) -> int:
        """calculate tokens"""
        try:
            if not data:
                return 0
                
            sample_size = min(10, len(data))
            sample_data = data[:sample_size]
            cleaned_sample = self._clean_batch_data(sample_data)
            sample_text = json.dumps(cleaned_sample, ensure_ascii=False)
            
            char_count = len(sample_text)
            if sample_size > 0:
                estimated_tokens_per_record = char_count / sample_size / 3.5  
                total_estimated_tokens = int(estimated_tokens_per_record * len(data) * 1.1)
            else:
                total_estimated_tokens = 0
            
            return max(1, total_estimated_tokens)
            
        except Exception as e:
            logging.error(f"Error estimating tokens: {str(e)}")
            return max(1, len(str(data)) // 3)

    def _create_smart_batches(self, all_records: list, max_tokens: int, target_batches: int) -> list:
        """ create optimization batches"""
        if not all_records:
            return []
        
        total_records = len(all_records)
        
        sample_batch = all_records[:min(50, total_records)]
        sample_tokens = self._estimate_tokens(sample_batch)
        
        if sample_tokens > 0:
            optimal_batch_size = int((max_tokens * len(sample_batch)) / sample_tokens * 0.9)
            optimal_batch_size = max(10, min(optimal_batch_size, total_records // max(1, target_batches)))
        else:
            optimal_batch_size = max(10, total_records // target_batches)
        
        logging.info(f"Calculated optimal batch size: {optimal_batch_size}")
        
        batches = []
        current_index = 0
        
        while current_index < total_records:
            
            end_index = min(current_index + optimal_batch_size, total_records)
            current_batch = all_records[current_index:end_index]
            
            tokens = self._estimate_tokens(current_batch)
            
            if tokens > max_tokens and len(current_batch) > 1:
                # loss size
                reduction_factor = max_tokens / tokens
                new_size = int(len(current_batch) * reduction_factor * 0.95)
                current_batch = current_batch[:max(1, new_size)]
                optimal_batch_size = len(current_batch)  
            
            batches.append(current_batch)
            current_index += len(current_batch)
            
            if len(batches) % 50 == 0:
                logging.info(f"Created {len(batches)} batches so far...")
        
        return batches

    def _save_batch(self, batch_data: list, batch_index: int, cache_key: str):
        """save batch"""
        try:
            cache_dir = f"temp_batches/{cache_key}"
            os.makedirs(cache_dir, exist_ok=True)
            batch_file = f"{cache_dir}/batch_{batch_index}.json"
            
            cleaned_data = self._clean_batch_data(batch_data)
            with open(batch_file, "w", encoding="utf-8") as f:
                json.dump(cleaned_data, f, ensure_ascii=False, separators=(',', ':'))
            
            return batch_file
        except Exception as e:
            logging.error(f"Error saving batch {batch_index}: {str(e)}")
            raise

    def _run(self, file_path: str, num_batches: int = 20, sleep_time: int = 0, 
             mime_type: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
             max_tokens_per_batch: int = 20000):  
        try:
            cache_key = self._get_cache_key(file_path)
            logging.info(f"Processing file: {file_path} with cache key: {cache_key}")
            
            existing_batches = self._check_existing_batches(cache_key)
            if existing_batches:
                logging.info(f"Using {len(existing_batches)} existing batch files")
                return existing_batches
            
            logging.info("Reading file...")
            if mime_type == "text/csv":
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path, engine="openpyxl")
            
            df = df.drop(columns=["Lot/Serial Number", "Product/Breadfast Barcode"], errors="ignore")
            all_records = df.to_dict(orient="records")
            
            logging.info(f"Total records: {len(all_records)}")
            
            batches = self._create_smart_batches(all_records, max_tokens_per_batch, num_batches)
            logging.info(f"Created {len(batches)} batches")
            
            result = []
            for i, batch in enumerate(batches):
                batch_file = self._save_batch(batch, i, cache_key)
                result.append(batch_file)
                
                if i % 100 == 0:
                    logging.info(f"Saved batch {i+1}/{len(batches)}")
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            logging.info(f"Successfully created {len(result)} batch files")
            return result
            
        except Exception as e:
            logging.error(f"Error processing file: {str(e)}")
            import traceback
            return f"Error processing file: {str(e)}\n{traceback.format_exc()}"

#=================================================


# from crewai.tools import BaseTool
# from typing import Type, List, Dict
# from pydantic import BaseModel, Field
# import os
# import json
# import logging
# from datetime import datetime, timedelta
# import gc
# import traceback



# class BatchProcessorInput(BaseModel):
#     """Input schema for BatchProcessor."""
#     input_directory: str = Field(..., description="Path to the directory containing batch JSON files")
#     output_directory: str = Field(default="results/inventory_management/batch_reports/", description="Directory to save batch reports")
#     final_report_path: str = Field(default="results/inventory_management/data_analysis_report.md", description="Path for the final consolidated report")

# class BatchProcessor(BaseTool):
#     name: str = "Batch Processor"
#     description: str = (
#         "Process all JSON batch files in a directory and generate individual batch reports "
#         "plus a consolidated final report. This tool handles large datasets split into multiple batches."
#     )
#     args_schema: Type[BaseModel] = BatchProcessorInput
    

#     def _run(self, input_directory: str, output_directory: str = "results/inventory_management/batch_reports/", 
#              final_report_path: str = "results/inventory_management/data_analysis_report.md") -> str:
#         """Process all batch files and generate reports."""
        
#         try:
#             # Setup logging
#             logging.basicConfig(level=logging.INFO)
#             logger = logging.getLogger(__name__)
            
#             # Ensure output directories exist
#             os.makedirs(output_directory, exist_ok=True)
#             os.makedirs(os.path.dirname(final_report_path), exist_ok=True)
            
#             # Check input directory
#             if not os.path.exists(input_directory):
#                 return f"ERROR: Input directory does not exist: {input_directory}"
            
#             # Get all batch files
#             batch_files = sorted([f for f in os.listdir(input_directory) if f.endswith('.json')])
            
#             if not batch_files:
#                 return f"ERROR: No JSON batch files found in {input_directory}"
            
#             logger.info(f"Found {len(batch_files)} batch files to process")
            
#             all_data = []
#             batch_reports = []
#             success_count = 0
            
#             # Process each batch
#             for i, batch_file in enumerate(batch_files):
#                 logger.info(f"Processing batch {i+1}/{len(batch_files)}: {batch_file}")
                
#                 try:
#                     # Extract batch number from filename
#                     batch_number = int(batch_file.replace('batch_', '').replace('.json', '')) + 1
#                 except ValueError:
#                     logger.warning(f"Invalid batch file name format: {batch_file}")
#                     continue
                
#                 batch_path = os.path.join(input_directory, batch_file)
                
#                 # Read batch data
#                 try:
#                     with open(batch_path, 'r', encoding='utf-8') as f:
#                         batch_data = json.load(f)
                    
#                     if not batch_data:
#                         logger.warning(f"Batch {batch_number} is empty")
#                         continue
                        
#                 except Exception as e:
#                     logger.error(f"Failed to read batch {batch_file}: {str(e)}")
#                     continue
                
#                 # Analyze batch
#                 try:
#                     batch_insights = self._analyze_batch(batch_data, batch_number)
                    
#                     if 'error' in batch_insights:
#                         logger.warning(f"Error analyzing batch {batch_number}: {batch_insights['error']}")
#                         continue
                        
#                 except Exception as e:
#                     logger.error(f"Failed to analyze batch {batch_number}: {str(e)}")
#                     continue
                
#                 # Save batch report
#                 batch_report_path = os.path.join(output_directory, f"batch_{batch_number}_report.md")
#                 try:
#                     self._save_batch_report(batch_insights, batch_report_path, batch_number)
#                     logger.info(f"Batch report saved: {batch_report_path}")
#                 except Exception as e:
#                     logger.error(f"Failed to save batch report {batch_number}: {str(e)}")
#                     continue
                
#                 # Collect results
#                 batch_reports.append({
#                     'batch_number': batch_number,
#                     'file': batch_file,
#                     'insights': batch_insights
#                 })
                
#                 all_data.extend(batch_data)
#                 success_count += 1
                
#                 # Memory cleanup
#                 batch_data = None
#                 batch_insights = None
#                 gc.collect()
            
#             # Generate final report
#             if success_count > 0:
#                 try:
#                     self._generate_final_report(batch_reports, all_data, final_report_path)
#                     logger.info(f"Final report generated: {final_report_path}")
                    
#                     return (f"SUCCESS: Processed {success_count}/{len(batch_files)} batches. "
#                            f"Reports saved in {output_directory}. "
#                            f"Final report: {final_report_path}")
                           
#                 except Exception as e:
#                     logger.error(f"Failed to generate final report: {str(e)}")
#                     return f"ERROR: Failed to generate final report: {str(e)}"
#             else:
#                 return "ERROR: No batches were successfully processed"
                
#         except Exception as e:
#             logger.error(f"BatchProcessor failed: {str(e)}")
#             traceback.print_exc()
#             return f"ERROR: BatchProcessor failed: {str(e)}"
    
#     def _analyze_batch(self, batch_data: List[Dict], batch_number: int) -> Dict:
#         """Analyze a single batch of data."""
#         try:
#             insights = {
#                 'batch_number': batch_number,
#                 'total_items': len(batch_data),
#                 'unique_skus': set(),
#                 'product_ids': set(),
#                 'product_names': set(),
#                 'missing_data': {'skus': 0, 'product_ids': 0, 'product_names': 0, 'barcodes': 0},
#                 'financial_categories': {},
#                 'locations': {},
#                 'total_available_quantity': 0.0,
#                 'near_expiry_products': []
#             }
            
#             current_date = datetime.now()
            
#             for item in batch_data:
#                 if not isinstance(item, dict):
#                     continue
                
#                 # SKU Analysis
#                 sku = item.get('Product/Internal Reference')
#                 if sku:
#                     insights['unique_skus'].add(str(sku))
#                 else:
#                     insights['missing_data']['skus'] += 1
                
#                 # Product ID (same as SKU)
#                 product_id = item.get('Product/Internal Reference')
#                 if product_id:
#                     insights['product_ids'].add(str(product_id))
#                 else:
#                     insights['missing_data']['product_ids'] += 1
                
#                 # Product Name
#                 product_name = item.get('Product/Name')
#                 if product_name:
#                     insights['product_names'].add(str(product_name))
#                 else:
#                     insights['missing_data']['product_names'] += 1
                
#                 # Barcode
#                 if not item.get('Product/Barcode'):
#                     insights['missing_data']['barcodes'] += 1
                
#                 # Financial Category
#                 category = item.get('Financial Category', 'Unknown')
#                 insights['financial_categories'][category] = insights['financial_categories'].get(category, 0) + 1
                
#                 # Location
#                 location = item.get('Location', 'Unknown')
#                 insights['locations'][location] = insights['locations'].get(location, 0) + 1
                
#                 # Quantity
#                 try:
#                     quantity = float(item.get('Available Quantity', 0.0))
#                     insights['total_available_quantity'] += quantity
#                 except (TypeError, ValueError):
#                     pass
                
#                 # Expiry Analysis
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
            
#             # Convert sets to counts and samples
#             insights['unique_skus_count'] = len(insights['unique_skus'])
#             insights['product_ids_count'] = len(insights['product_ids'])
#             insights['product_names_count'] = len(insights['product_names'])
#             insights['unique_skus'] = list(insights['unique_skus'])[:10]
#             insights['product_ids'] = list(insights['product_ids'])[:10]
#             insights['product_names'] = list(insights['product_names'])[:10]
#             insights['near_expiry_count'] = len(insights['near_expiry_products'])
            
#             return insights
            
#         except Exception as e:
#             return {'batch_number': batch_number, 'error': str(e)}
    
#     def _save_batch_report(self, insights: Dict, report_path: str, batch_number: int) -> None:
#         """Save individual batch report."""
#         with open(report_path, 'w', encoding='utf-8') as f:
#             f.write(f"# Batch {batch_number} Analysis Report\n\n")
#             f.write(f"**Generation Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
#             f.write(f"**Total Items**: {insights.get('total_items', 0)}\n")
#             f.write(f"**Unique SKUs**: {insights.get('unique_skus_count', 0)}\n")
#             f.write(f"**Unique Products**: {insights.get('product_names_count', 0)}\n")
#             f.write(f"**Total Available Quantity**: {insights.get('total_available_quantity', 0.0):.2f}\n")
#             f.write(f"**Near Expiry Products**: {insights.get('near_expiry_count', 0)}\n\n")
            
#             # Sample data
#             f.write("## Sample Data\n")
#             f.write(f"**Sample SKUs**: {', '.join(insights.get('unique_skus', []))}\n")
#             f.write(f"**Sample Products**: {', '.join(insights.get('product_names', []))}\n\n")
            
#             # Categories
#             f.write("## Financial Categories\n")
#             for category, count in insights.get('financial_categories', {}).items():
#                 f.write(f"- **{category}**: {count} items\n")
            
#             # Missing data
#             f.write("\n## Missing Data\n")
#             missing = insights.get('missing_data', {})
#             for key, value in missing.items():
#                 f.write(f"- **{key.capitalize()}**: {value} missing\n")
            
#             if 'error' in insights:
#                 f.write(f"\n## Errors\n```\n{insights['error']}\n```\n")
    
#     def _generate_final_report(self, batch_reports: List[Dict], all_data: List[Dict], final_report_path: str) -> None:
#         """Generate final consolidated report."""
#         with open(final_report_path, 'w', encoding='utf-8') as f:
#             f.write("# Final Inventory Data Analysis Report\n\n")
#             f.write(f"**Generation Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
#             f.write(f"**Total Batches Processed**: {len(batch_reports)}\n")
#             f.write(f"**Total Items Processed**: {len(all_data)}\n\n")
            
#             # Aggregate data
#             all_skus = set()
#             all_products = set()
#             all_categories = {}
#             all_locations = {}
#             total_quantity = 0.0
#             total_near_expiry = 0
#             total_missing = {'skus': 0, 'product_ids': 0, 'product_names': 0, 'barcodes': 0}
            
#             for report in batch_reports:
#                 insights = report['insights']
#                 if 'error' not in insights:
#                     all_skus.update(insights.get('unique_skus', []))
#                     all_products.update(insights.get('product_names', []))
                    
#                     # Aggregate categories
#                     for cat, count in insights.get('financial_categories', {}).items():
#                         all_categories[cat] = all_categories.get(cat, 0) + count
                    
#                     # Aggregate locations
#                     for loc, count in insights.get('locations', {}).items():
#                         all_locations[loc] = all_locations.get(loc, 0) + count
                    
#                     total_quantity += insights.get('total_available_quantity', 0.0)
#                     total_near_expiry += insights.get('near_expiry_count', 0)
                    
#                     # Missing data
#                     missing = insights.get('missing_data', {})
#                     for key in total_missing:
#                         total_missing[key] += missing.get(key, 0)
            
#             # Write aggregated insights
#             f.write("## Aggregated Insights\n")
#             f.write(f"- **Total Unique SKUs**: {len(all_skus)}\n")
#             f.write(f"- **Total Unique Products**: {len(all_products)}\n")
#             f.write(f"- **Total Available Quantity**: {total_quantity:.2f}\n")
#             f.write(f"- **Total Near Expiry Products**: {total_near_expiry}\n\n")
            
#             # Top categories
#             f.write("## Top Financial Categories\n")
#             sorted_categories = sorted(all_categories.items(), key=lambda x: x[1], reverse=True)
#             for category, count in sorted_categories[:10]:
#                 f.write(f"- **{category}**: {count} items\n")
            
#             # Locations
#             f.write("\n## Storage Locations\n")
#             for location, count in all_locations.items():
#                 f.write(f"- **{location}**: {count} items\n")
            
#             # Missing data summary
#             f.write("\n## Data Quality Issues\n")
#             for key, value in total_missing.items():
#                 f.write(f"- **{key.capitalize()} missing**: {value}\n")
            
#             # Batch summary
#             f.write("\n## Batch Processing Summary\n")
#             successful_batches = [r for r in batch_reports if 'error' not in r['insights']]
#             failed_batches = [r for r in batch_reports if 'error' in r['insights']]
            
#             f.write(f"- **Successfully processed**: {len(successful_batches)} batches\n")
#             f.write(f"- **Failed to process**: {len(failed_batches)} batches\n")
            
#             if failed_batches:
#                 f.write("\n### Failed Batches\n")
#                 for report in failed_batches:
#                     f.write(f"- Batch {report['batch_number']}: {report['insights']['error']}\n")
                    
        
#==================================================================

# from crewai.tools import BaseTool
# from typing import Type, List, Dict
# from pydantic import BaseModel, Field
# import os
# import json
# import logging
# from datetime import datetime, timedelta
# import gc
# import traceback


# class BatchProcessorInput(BaseModel):
#     """Input schema for BatchProcessor."""
#     input_directory: str = Field(..., description="Path to the directory containing batch JSON files")
#     output_directory: str = Field(default="results/inventory_management/batch_reports/", description="Directory to save batch reports")
#     final_report_path: str = Field(default="results/inventory_management/data_analysis_report.md", description="Path for the final consolidated report")


# class BatchProcessor(BaseTool):
#     name: str = "Batch Processor"
#     description: str = (
#         "Process all JSON batch files in a directory and generate individual batch reports "
#         "plus a consolidated final report. This tool handles large datasets split into multiple batches."
#     )
#     args_schema: Type[BaseModel] = BatchProcessorInput

#     def _run(self, input_directory: str, output_directory: str = "results/inventory_management/batch_reports/",
#              final_report_path: str = "results/inventory_management/data_analysis_report.md") -> str:

#         try:
#             # Setup logging
#             logging.basicConfig(level=logging.INFO)
#             logger = logging.getLogger(__name__)

#             # Ensure output directories exist
#             os.makedirs(output_directory, exist_ok=True)
#             os.makedirs(os.path.dirname(final_report_path), exist_ok=True)

#             # Check input directory
#             if not os.path.exists(input_directory):
#                 return f"ERROR: Input directory does not exist: {input_directory}"

#             # Get all batch files
#             batch_files = sorted([f for f in os.listdir(input_directory) if f.endswith('.json')])

#             if not batch_files:
#                 return f"ERROR: No JSON batch files found in {input_directory}"

#             logger.info(f"Found {len(batch_files)} batch files to process")

#             # Load existing cache
#             cache_file_path = os.path.join(output_directory, "batch_cache.json")
#             file_cache = {}
#             if os.path.exists(cache_file_path):
#                 try:
#                     with open(cache_file_path, 'r', encoding='utf-8') as f:
#                         file_cache = json.load(f)
#                 except Exception as e:
#                     logger.warning(f"Failed to load cache: {e}")

#             all_data = []
#             batch_reports = []
#             success_count = 0

#             for i, batch_file in enumerate(batch_files):
#                 logger.info(f"Processing batch {i + 1}/{len(batch_files)}: {batch_file}")
#                 batch_path = os.path.join(input_directory, batch_file)
#                 cache_key = self._get_cache_key(batch_path)

#                 if batch_file in file_cache and file_cache[batch_file] == cache_key:
#                     logger.info(f"Skipping cached batch: {batch_file}")
#                     continue

#                 try:
#                     batch_number = int(batch_file.replace('batch_', '').replace('.json', '')) + 1
#                 except ValueError:
#                     logger.warning(f"Invalid batch file name format: {batch_file}")
#                     continue

#                 try:
#                     with open(batch_path, 'r', encoding='utf-8') as f:
#                         batch_data = json.load(f)

#                     if not batch_data:
#                         logger.warning(f"Batch {batch_number} is empty")
#                         continue
#                 except Exception as e:
#                     logger.error(f"Failed to read batch {batch_file}: {str(e)}")
#                     continue

#                 try:
#                     batch_insights = self._analyze_batch(batch_data, batch_number)
#                     if 'error' in batch_insights:
#                         logger.warning(f"Error analyzing batch {batch_number}: {batch_insights['error']}")
#                         continue
#                 except Exception as e:
#                     logger.error(f"Failed to analyze batch {batch_number}: {str(e)}")
#                     continue

#                 batch_report_path = os.path.join(output_directory, f"batch_{batch_number}_report.md")
#                 try:
#                     self._save_batch_report(batch_insights, batch_report_path, batch_number)
#                     logger.info(f"Batch report saved: {batch_report_path}")
#                 except Exception as e:
#                     logger.error(f"Failed to save batch report {batch_number}: {str(e)}")
#                     continue

#                 # Update cache
#                 file_cache[batch_file] = cache_key

#                 batch_reports.append({
#                     'batch_number': batch_number,
#                     'file': batch_file,
#                     'insights': batch_insights
#                 })
#                 all_data.extend(batch_data)
#                 success_count += 1

#                 batch_data = None
#                 batch_insights = None
#                 gc.collect()

#             # Generate final report
#             if success_count > 0:
#                 try:
#                     self._generate_final_report(batch_reports, all_data, final_report_path)
#                     logger.info(f"Final report generated: {final_report_path}")

#                     # Save updated cache
#                     try:
#                         with open(cache_file_path, 'w', encoding='utf-8') as f:
#                             json.dump(file_cache, f, indent=2)
#                         logger.info(f"Cache saved to {cache_file_path}")
#                     except Exception as e:
#                         logger.warning(f"Failed to save cache: {e}")

#                     return (f"SUCCESS: Processed {success_count}/{len(batch_files)} batches. "
#                             f"Reports saved in {output_directory}. "
#                             f"Final report: {final_report_path}")
#                 except Exception as e:
#                     logger.error(f"Failed to generate final report: {str(e)}")
#                     return f"ERROR: Failed to generate final report: {str(e)}"
#             else:
#                 return "ERROR: No batches were successfully processed"

#         except Exception as e:
#             logger.error(f"BatchProcessor failed: {str(e)}")
#             traceback.print_exc()
#             return f"ERROR: BatchProcessor failed: {str(e)}"

#     def _get_cache_key(self, file_path: str) -> str:
#         """Create a unique cache key based on file modification time and size."""
#         try:
#             stat = os.stat(file_path)
#             return f"{os.path.basename(file_path)}_{stat.st_mtime}_{stat.st_size}"
#         except Exception:
#             return f"{os.path.basename(file_path)}_no_stat"

#     def _analyze_batch(self, batch_data: List[Dict], batch_number: int) -> Dict:
#         """Analyze a single batch of data."""
#         try:
#             insights = {
#                 'batch_number': batch_number,
#                 'total_items': len(batch_data),
#                 'unique_skus': set(),
#                 'product_ids': set(),
#                 'product_names': set(),
#                 'missing_data': {'skus': 0, 'product_ids': 0, 'product_names': 0, 'barcodes': 0},
#                 'financial_categories': {},
#                 'locations': {},
#                 'total_available_quantity': 0.0,
#                 'near_expiry_products': []
#             }

#             current_date = datetime.now()

#             for item in batch_data:
#                 if not isinstance(item, dict):
#                     continue

#                 sku = item.get('Product/Internal Reference')
#                 if sku:
#                     insights['unique_skus'].add(str(sku))
#                 else:
#                     insights['missing_data']['skus'] += 1

#                 product_id = item.get('Product/Internal Reference')
#                 if product_id:
#                     insights['product_ids'].add(str(product_id))
#                 else:
#                     insights['missing_data']['product_ids'] += 1

#                 product_name = item.get('Product/Name')
#                 if product_name:
#                     insights['product_names'].add(str(product_name))
#                 else:
#                     insights['missing_data']['product_names'] += 1

#                 if not item.get('Product/Barcode'):
#                     insights['missing_data']['barcodes'] += 1

#                 category = item.get('Financial Category', 'Unknown')
#                 insights['financial_categories'][category] = insights['financial_categories'].get(category, 0) + 1

#                 location = item.get('Location', 'Unknown')
#                 insights['locations'][location] = insights['locations'].get(location, 0) + 1

#                 try:
#                     quantity = float(item.get('Available Quantity', 0.0))
#                     insights['total_available_quantity'] += quantity
#                 except (TypeError, ValueError):
#                     pass

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
#             return {'batch_number': batch_number, 'error': str(e)}

#     def _save_batch_report(self, insights: Dict, report_path: str, batch_number: int) -> None:
#         """Save individual batch report."""
#         with open(report_path, 'w', encoding='utf-8') as f:
#             f.write(f"# Batch {batch_number} Analysis Report\n\n")
#             f.write(f"**Generation Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
#             f.write(f"**Total Items**: {insights.get('total_items', 0)}\n")
#             f.write(f"**Unique SKUs**: {insights.get('unique_skus_count', 0)}\n")
#             f.write(f"**Unique Products**: {insights.get('product_names_count', 0)}\n")
#             f.write(f"**Total Available Quantity**: {insights.get('total_available_quantity', 0.0):.2f}\n")
#             f.write(f"**Near Expiry Products**: {insights.get('near_expiry_count', 0)}\n\n")

#             f.write("## Sample Data\n")
#             f.write(f"**Sample SKUs**: {', '.join(insights.get('unique_skus', []))}\n")
#             f.write(f"**Sample Products**: {', '.join(insights.get('product_names', []))}\n\n")

#             f.write("## Financial Categories\n")
#             for category, count in insights.get('financial_categories', {}).items():
#                 f.write(f"- **{category}**: {count} items\n")

#             f.write("\n## Missing Data\n")
#             missing = insights.get('missing_data', {})
#             for key, value in missing.items():
#                 f.write(f"- **{key.capitalize()}**: {value} missing\n")

#             if 'error' in insights:
#                 f.write(f"\n## Errors\n```\n{insights['error']}\n```\n")

#     def _generate_final_report(self, batch_reports: List[Dict], all_data: List[Dict], final_report_path: str) -> None:
#         """Generate final consolidated report."""
#         with open(final_report_path, 'w', encoding='utf-8') as f:
#             f.write("# Final Inventory Data Analysis Report\n\n")
#             f.write(f"**Generation Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
#             f.write(f"**Total Batches Processed**: {len(batch_reports)}\n")
#             f.write(f"**Total Items Processed**: {len(all_data)}\n\n")

#             all_skus = set()
#             all_products = set()
#             all_categories = {}
#             all_locations = {}
#             total_quantity = 0.0
#             total_near_expiry = 0
#             total_missing = {'skus': 0, 'product_ids': 0, 'product_names': 0, 'barcodes': 0}

#             for report in batch_reports:
#                 insights = report['insights']
#                 if 'error' not in insights:
#                     all_skus.update(insights.get('unique_skus', []))
#                     all_products.update(insights.get('product_names', []))

#                     for cat, count in insights.get('financial_categories', {}).items():
#                         all_categories[cat] = all_categories.get(cat, 0) + count

#                     for loc, count in insights.get('locations', {}).items():
#                         all_locations[loc] = all_locations.get(loc, 0) + count

#                     total_quantity += insights.get('total_available_quantity', 0.0)
#                     total_near_expiry += insights.get('near_expiry_count', 0)

#                     missing = insights.get('missing_data', {})
#                     for key in total_missing:
#                         total_missing[key] += missing.get(key, 0)

#             f.write("## Aggregated Insights\n")
#             f.write(f"- **Total Unique SKUs**: {len(all_skus)}\n")
#             f.write(f"- **Total Unique Products**: {len(all_products)}\n")
#             f.write(f"- **Total Available Quantity**: {total_quantity:.2f}\n")
#             f.write(f"- **Total Near Expiry Products**: {total_near_expiry}\n\n")

#             f.write("## Top Financial Categories\n")
#             sorted_categories = sorted(all_categories.items(), key=lambda x: x[1], reverse=True)
#             for category, count in sorted_categories[:10]:
#                 f.write(f"- **{category}**: {count} items\n")

#             f.write("\n## sample Storage Locations\n")
#             counter = 0
#             for location, count in all_locations.items():
#                 f.write(f"- **{location}**: {count} items\n")
#                 counter+=1
#                 if counter ==10:
#                     break
                
#             f.write("\n## Data Quality Issues\n")
#             for key, value in total_missing.items():
#                 f.write(f"- **{key.capitalize()} missing**: {value}\n")

#             f.write("\n## Batch Processing Summary\n")
#             successful_batches = [r for r in batch_reports if 'error' not in r['insights']]
#             failed_batches = [r for r in batch_reports if 'error' in r['insights']]

#             f.write(f"- **Successfully processed**: {len(successful_batches)} batches\n")
#             f.write(f"- **Failed to process**: {len(failed_batches)} batches\n")

#             if failed_batches:
#                 f.write("\n### Failed Batches\n")
#                 for report in failed_batches:
#                     f.write(f"- Batch {report['batch_number']}: {report['insights']['error']}\n")

#=======================================================================

from crewai.tools import BaseTool
from typing import Type, List, Dict
from pydantic import BaseModel, Field
import os
import json
import logging
from datetime import datetime, timedelta
import gc
import traceback
import hashlib

class BatchProcessorInput(BaseModel):
    """Input schema for BatchProcessor."""
    input_directory: str = Field(..., description="Path to the directory containing batch JSON files")
    output_directory: str = Field(default="results/Batches/", description="Directory to save batch reports")
    final_report_path: str = Field(default="results/inventory_management/data_analysis_report.md", description="Path for the final consolidated report")

class BatchProcessor(BaseTool):
    name: str = "Batch Processor"
    description: str = (
        "Process all JSON batch files in a directory and generate individual batch reports "
        "plus a consolidated final report. This tool handles large datasets split into multiple batches."
    )
    args_schema: Type[BaseModel] = BatchProcessorInput
    
    # def _get_cache_key(self, input_directory: str) -> str:
    #     """Create cache key for the input directory."""
    #     try:
    #         stat = os.stat(input_directory)
    #         dir_name = os.path.basename(input_directory)
    #         return f"cache_{dir_name}_{stat.st_mtime}_{stat.st_size}"
    #     except Exception as e:
    #         logging.error(f"Failed to generate cache key for directory {input_directory}: {str(e)}")
    #         return f"cache_{os.path.basename(input_directory)}_no_stat"
    


    def _get_cache_key(self, input_directory: str) -> str:
        try:
            hash_input = ""
            for filename in sorted(os.listdir(input_directory)):
                if filename.endswith('.json'):
                    path = os.path.join(input_directory, filename)
                    if os.path.isfile(path):
                        stat = os.stat(path)
                        hash_input += f"{filename}_{stat.st_mtime}_{stat.st_size}|"
            hash_digest = hashlib.md5(hash_input.encode()).hexdigest()
            return f"cache_{os.path.basename(input_directory)}_{hash_digest}"
        except Exception as e:
            logging.error(f"Failed to generate cache key for directory {input_directory}: {str(e)}")
            return f"cache_{os.path.basename(input_directory)}_no_stat"


    def _run(self, input_directory: str, output_directory: str = "results/Batches/", 
             final_report_path: str = "results/inventory_management/data_analysis_report.md") -> str:
        """Process all batch files and generate reports."""
        
        try:
            # Setup logging
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            
            # Generate unique cache folder
            cache_key = self._get_cache_key(input_directory)
            cache_directory = os.path.join(output_directory, cache_key)
            
            # Ensure output and cache directories exist
            os.makedirs(output_directory, exist_ok=True)
            os.makedirs(cache_directory, exist_ok=True)
            os.makedirs(os.path.dirname(final_report_path), exist_ok=True)
            
            # Check input directory
            if not os.path.exists(input_directory):
                return f"ERROR: Input directory does not exist: {input_directory}"
            
            # Get all batch files
            batch_files = sorted([f for f in os.listdir(input_directory) if f.endswith('.json')])
            
            if not batch_files:
                return f"ERROR: No JSON batch files found in {input_directory}"
            
            logger.info(f"Found {len(batch_files)} batch files to process")
            
            all_data = []
            batch_reports = []
            success_count = 0
            
            # Process each batch
            for i, batch_file in enumerate(batch_files):
                logger.info(f"Processing batch {i+1}/{len(batch_files)}: {batch_file}")
                
                try:
                    # Extract batch number from filename
                    batch_number = int(batch_file.replace('batch_', '').replace('.json', '')) + 1
                except ValueError:
                    logger.warning(f"Invalid batch file name format: {batch_file}")
                    continue
                
                batch_path = os.path.join(input_directory, batch_file)
                
                # Read batch data
                try:
                    with open(batch_path, 'r', encoding='utf-8') as f:
                        batch_data = json.load(f)
                    
                    if not batch_data:
                        logger.warning(f"Batch {batch_number} is empty")
                        continue
                        
                except Exception as e:
                    logger.error(f"Failed to read batch {batch_file}: {str(e)}")
                    continue
                
                # Analyze batch
                try:
                    batch_insights = self._analyze_batch(batch_data, batch_number)
                    
                    if 'error' in batch_insights:
                        logger.warning(f"Error analyzing batch {batch_number}: {batch_insights['error']}")
                        continue
                        
                except Exception as e:
                    logger.error(f"Failed to analyze batch {batch_number}: {str(e)}")
                    continue
                
                # Save batch report in cache directory
                batch_report_path = os.path.join(cache_directory, f"batch_{batch_number}_report.md")
                try:
                    self._save_batch_report(batch_insights, batch_report_path, batch_number)
                    logger.info(f"Batch report saved: {batch_report_path}")
                except Exception as e:
                    logger.error(f"Failed to save batch report {batch_number}: {str(e)}")
                    continue
                
                # Collect results
                batch_reports.append({
                    'batch_number': batch_number,
                    'file': batch_file,
                    'insights': batch_insights
                })
                
                all_data.extend(batch_data)
                success_count += 1
                
                # Memory cleanup
                batch_data = None
                batch_insights = None
                gc.collect()
            
            # Generate final report
            if success_count > 0:
                try:
                    self._generate_final_report(batch_reports, all_data, final_report_path)
                    logger.info(f"Final report generated: {final_report_path}")
                    
                    return (f"SUCCESS: Processed {success_count}/{len(batch_files)} batches. "
                           f"Reports saved in {cache_directory}. "
                           f"Final report: {final_report_path}")
                           
                except Exception as e:
                    logger.error(f"Failed to generate final report: {str(e)}")
                    return f"ERROR: Failed to generate final report: {str(e)}"
            else:
                return "ERROR: No batches were successfully processed"
                
        except Exception as e:
            logger.error(f"BatchProcessor failed: {str(e)}")
            traceback.print_exc()
            return f"ERROR: BatchProcessor failed: {str(e)}"
    
    def _analyze_batch(self, batch_data: List[Dict], batch_number: int) -> Dict:
        """Analyze a single batch of data."""
        try:
            insights = {
                'batch_number': batch_number,
                'total_items': len(batch_data),
                'unique_skus': set(),
                'product_ids': set(),
                'product_names': set(),
                'missing_data': {'skus': 0, 'product_ids': 0, 'product_names': 0, 'barcodes': 0},
                'financial_categories': {},
                'locations': {},
                'total_available_quantity': 0.0,
                'near_expiry_products': []
            }
            
            current_date = datetime.now()
            
            for item in batch_data:
                if not isinstance(item, dict):
                    continue
                
                # SKU Analysis
                sku = item.get('Product/Internal Reference')
                if sku:
                    insights['unique_skus'].add(str(sku))
                else:
                    insights['missing_data']['skus'] += 1
                
                # Product ID (same as SKU)
                product_id = item.get('Product/Internal Reference')
                if product_id:
                    insights['product_ids'].add(str(product_id))
                else:
                    insights['missing_data']['product_ids'] += 1
                
                # Product Name
                product_name = item.get('Product/Name')
                if product_name:
                    insights['product_names'].add(str(product_name))
                else:
                    insights['missing_data']['product_names'] += 1
                
                # Barcode
                if not item.get('Product/Barcode'):
                    insights['missing_data']['barcodes'] += 1
                
                # Financial Category
                category = item.get('Financial Category', 'Unknown')
                insights['financial_categories'][category] = insights['financial_categories'].get(category, 0) + 1
                
                # Location
                location = item.get('Location', 'Unknown')
                insights['locations'][location] = insights['locations'].get(location, 0) + 1
                
                # Quantity
                try:
                    quantity = float(item.get('Available Quantity', 0.0))
                    insights['total_available_quantity'] += quantity
                except (TypeError, ValueError):
                    pass
                
                # Expiry Analysis
                expiry_date = item.get('Lot/Serial Number/Expiration Date')
                if expiry_date:
                    try:
                        expiry = datetime.strptime(expiry_date, '%Y-%m-%d %H:%M:%S')
                        if expiry < current_date + timedelta(days=90):
                            insights['near_expiry_products'].append({
                                'sku': sku,
                                'name': product_name,
                                'expiry_date': expiry_date
                            })
                    except ValueError:
                        pass
            
            # Convert sets to counts and samples
            insights['unique_skus_count'] = len(insights['unique_skus'])
            insights['product_ids_count'] = len(insights['product_ids'])
            insights['product_names_count'] = len(insights['product_names'])
            insights['unique_skus'] = list(insights['unique_skus'])[:10]
            insights['product_ids'] = list(insights['product_ids'])[:10]
            insights['product_names'] = list(insights['product_names'])[:10]
            insights['near_expiry_count'] = len(insights['near_expiry_products'])
            
            return insights
            
        except Exception as e:
            return {'batch_number': batch_number, 'error': str(e)}
    
    def _save_batch_report(self, insights: Dict, report_path: str, batch_number: int) -> None:
        """Save individual batch report."""
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Batch {batch_number} Analysis Report\n\n")
            f.write(f"**Generation Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total Items**: {insights.get('total_items', 0)}\n")
            f.write(f"**Unique SKUs**: {insights.get('unique_skus_count', 0)}\n")
            f.write(f"**Unique Products**: {insights.get('product_names_count', 0)}\n")
            f.write(f"**Total Available Quantity**: {insights.get('total_available_quantity', 0.0):.2f}\n")
            f.write(f"**Near Expiry Products**: {insights.get('near_expiry_count', 0)}\n\n")
            
            # Sample data
            f.write("## Sample Data\n")
            f.write(f"**Sample SKUs**: {', '.join(insights.get('unique_skus', []))}\n")
            f.write(f"**Sample Products**: {', '.join(insights.get('product_names', []))}\n\n")
            
            # Categories
            f.write("## Financial Categories\n")
            for category, count in insights.get('financial_categories', {}).items():
                f.write(f"- **{category}**: {count} items\n")
            
            # Missing data
            f.write("\n## Missing Data\n")
            for key, value in insights.get('missing_data', {}).items():
                f.write(f"- **{key.capitalize()}**: {value} missing\n")
            
            if 'error' in insights:
                f.write(f"\n## Errors\n```\n{insights['error']}\n```\n")
    
    def _generate_final_report(self, batch_reports: List[Dict], all_data: List[Dict], final_report_path: str) -> None:
        """Generate final consolidated report."""
        with open(final_report_path, 'w', encoding='utf-8') as f:
            f.write("# Final Inventory Data Analysis Report\n\n")
            f.write(f"**Generation Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total Batches Processed**: {len(batch_reports)}\n")
            f.write(f"**Total Items Processed**: {len(all_data)}\n\n")
            
            # Aggregate data
            all_skus = set()
            all_products = set()
            all_categories = {}
            all_locations = {}
            total_quantity = 0.0
            total_near_expiry = 0
            total_missing = {'skus': 0, 'product_ids': 0, 'product_names': 0, 'barcodes': 0}
            
            for report in batch_reports:
                insights = report['insights']
                if 'error' not in insights:
                    all_skus.update(insights.get('unique_skus', []))
                    all_products.update(insights.get('product_names', []))
                    
                    # Aggregate categories
                    for cat, count in insights.get('financial_categories', {}).items():
                        all_categories[cat] = all_categories.get(cat, 0) + count
                    
                    # Aggregate locations
                    for loc, count in insights.get('locations', {}).items():
                        all_locations[loc] = all_locations.get(loc, 0) + count
                    
                    total_quantity += insights.get('total_available_quantity', 0.0)
                    total_near_expiry += insights.get('near_expiry_count', 0)
                    
                    # Missing data
                    missing = insights.get('missing_data', {})
                    for key in total_missing:
                        total_missing[key] += missing.get(key, 0)
            
            # Write aggregated insights
            f.write("## Aggregated Insights\n")
            f.write(f"- **Total Unique SKUs**: {len(all_skus)}\n")
            f.write(f"- **Total Unique Products**: {len(all_products)}\n")
            f.write(f"- **Total Available Quantity**: {total_quantity:.2f}\n")
            f.write(f"- **Total Near Expiry Products**: {total_near_expiry}\n\n")
            
            # Top categories
            f.write("## Top Financial Categories\n")
            sorted_categories = sorted(all_categories.items(), key=lambda x: x[1], reverse=True)
            for category, count in sorted_categories[:10]:
                f.write(f"- **{category}**: {count} items\n")
            
            # Locations
            f.write("\n##Sample Storage Locations\n")
            counter =0
            for location, count in all_locations.items():
                f.write(f"- **{location}**: {count} items\n")
                counter+=1
                if counter ==10:
                    break
            
            # Missing data summary
            f.write("\n## Data Quality Issues\n")
            for key, value in total_missing.items():
                f.write(f"- **{key.capitalize()} missing**: {value}\n")
            
            # Batch summary
            f.write("\n## Batch Processing Summary\n")
            successful_batches = [r for r in batch_reports if 'error' not in r['insights']]
            failed_batches = [r for r in batch_reports if 'error' in r['insights']]
            
            f.write(f"- **Successfully processed**: {len(successful_batches)} batches\n")
            f.write(f"- **Failed to process**: {len(failed_batches)} batches\n")
            
            if failed_batches:
                f.write("\n### Failed Batches\n")
                for report in failed_batches:
                    f.write(f"- Batch {report['batch_number']}: {report['insights']['error']}\n")

#===================================================================


class JsonBatchFileReader(BaseTool):
    name: str = "JSON Batch File Reader"
    description: str = "Reads JSON batch files from a directory and returns cleaned data batch by batch for analysis."
    args_schema: Type[BaseModel] = JsonBatchFileReaderSchema

    def _clean_batch_data(self, batch_data: list) -> list:
        """Convert non-serializable types and handle missing values."""
        cleaned_data = []
        for record in batch_data:
            if not isinstance(record, dict):
                logging.warning(f"Skipping non-dict record: {record}")
                continue

            cleaned_record = {}
            for key, value in record.items():
                try:
                    if isinstance(value, pd.Timestamp):
                        cleaned_record[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                    elif pd.isna(value) or value is None:
                        cleaned_record[key] = ""
                    elif isinstance(value, (int, float, str, bool)):
                        cleaned_record[key] = value
                    else:
                        cleaned_record[key] = str(value)
                except Exception as e:
                    logging.warning(f"Error cleaning field {key}: {str(e)}")
                    cleaned_record[key] = ""
            
            cleaned_data.append(cleaned_record)
        return cleaned_data

    def _run(self, file_path: str) -> list:
        """Read a single JSON file and return cleaned data."""
        try:
            logging.info(f"Reading JSON file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                logging.error(f"Data in {file_path} is not a list: {type(data)}")
                return []
            
            cleaned_data = self._clean_batch_data(data)
            logging.info(f"Successfully read and cleaned {len(cleaned_data)} records from {file_path}")
            return cleaned_data
        
        except Exception as e:
            logging.error(f"Failed to read {file_path}: {str(e)}")
            return []

    def read_file(self, file_path: str) -> list:
        """Simple method to read a single file (used internally or for testing)."""
        return self._run(file_path)

    def read_batches(self, folder_path: str) -> List[list]:
        """
        Read all JSON batch files in a directory one by one.
        Returns a list of batches (each batch is a list of records).
        """
        all_batches = []
        try:
            files = sorted([
                os.path.join(folder_path, file)
                for file in os.listdir(folder_path)
                if file.endswith('.json')
            ])

            if not files:
                logging.warning(f"No JSON files found in directory: {folder_path}")
                return []

            logging.info(f"Found {len(files)} batch files in {folder_path}")

            for i, file_path in enumerate(files):
                logging.info(f"Reading batch {i + 1}/{len(files)}: {file_path}")
                batch_data = self._run(file_path)
                if batch_data:
                    all_batches.append(batch_data)

            logging.info(f"Finished reading {len(all_batches)} batches")
            return all_batches

        except Exception as e:
            logging.error(f"Error reading batches from folder {folder_path}: {str(e)}")
            return []

