
from crewai.tools import BaseTool
from .Schema.BatchProcessingSchema import BatchProcessorSchema
from typing import Type, List, Dict
from pydantic import BaseModel
import os
import json
import logging
from datetime import datetime, timedelta
import gc
import traceback
import hashlib



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_processing.log'),
        logging.StreamHandler()
    ]
)

class BatchProcessor(BaseTool):
    name: str = "Batch Processor"
    description: str = (
        "Process all JSON batch files in a directory and generate individual batch reports "
        "plus a consolidated final report. This tool handles large datasets split into multiple batches."
    )
    args_schema: Type[BaseModel] = BatchProcessorSchema
    
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
    
    def _run(
        self,
        input_directory: str,
        output_directory: str = "results/Mini_reports",
        final_report_path: str = "results/inventory_management/data_analysis_report.md"
    ) -> str:

        """Process all batch files and generate reports.
        Simple Analysis:
            aggregated insights
            Top Financial Categories
            Data Quality Issues
            Batch Processing Summary
            Failed Batches
            
        Advanced questions:
            Near expiry or removal within 6 months
            Urgent reorder
            Duplicate SKUs
          
    """
        
        try:
            # Setup logging
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            
            if not os.path.exists(output_directory):
                os.makedirs(output_directory, exist_ok=True)
                
            # Generate unique cache folder
            cache_key = self._get_cache_key(input_directory)
            cache_directory = os.path.join(output_directory, cache_key)
            
            # Ensure output and cache directories exist
            os.makedirs(cache_directory, exist_ok=True)
            dir_path = os.path.dirname(final_report_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

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
                        if expiry < current_date + timedelta(days=30):
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
                
#===========================================================================================                             
                    
    def _generate_final_report(self, batch_reports: List[Dict], all_data: List[Dict], final_report_path: str) -> None:
        """Generate final consolidated report with advanced questions."""
        with open(final_report_path, 'w', encoding='utf-8') as f:
            f.write("# Final Inventory Data Analysis Report\n\n")
            f.write(f"**Generation Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total Items Processed**: {len(all_data)}\n\n")
            
# =================================== Basics Insights ===========================================
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

                    for cat, count in insights.get('financial_categories', {}).items():
                        all_categories[cat] = all_categories.get(cat, 0) + count

                    for loc, count in insights.get('locations', {}).items():
                        all_locations[loc] = all_locations.get(loc, 0) + count

                    total_quantity += insights.get('total_available_quantity', 0.0)
                    total_near_expiry += insights.get('near_expiry_count', 0)

                    missing = insights.get('missing_data', {})
                    for key in total_missing:
                        total_missing[key] += missing.get(key, 0)
                        
            # Aggregated Insights
            f.write("## Aggregated Insights\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| Total Unique Products | {len(all_products)} |\n")
            f.write(f"| Total Available Quantity | {total_quantity:.2f} |\n")
            f.write(f"| Total Near Expiry Products During Next Month | {total_near_expiry} |\n\n")

            # Top categories
            f.write("## Financial Categories\n")
            f.write("| category | count |\n")
            f.write("|--------|-------|\n")
            sorted_categories = sorted(all_categories.items(), key=lambda x: x[1], reverse=True)
            for category, count in sorted_categories:
                f.write(f"| {category}  | {count} items |\n")

            # Data quality issues
            f.write("\n## Data Quality Issues\n")
            f.write("| Colunm Name | missing Count |\n")
            f.write("|--------|-------|\n")
            for key, value in total_missing.items():
                f.write(f"| {key.capitalize()}  | {value}  |\n")
                
                    
# ==================================== Advanced Questions ==========================================

            f.write("\n# Advanced Analysis\n")
            def parse_date(date_str):
                """Try parsing date from multiple common formats; return None if it fails."""
                if not date_str:
                    return None
                for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'):
                    try:
                        return datetime.strptime(date_str, fmt)
                    except:
                        pass
                return None

            current_date = datetime.now()
                       
            q_expired = [
            item for item in all_data
            if (
                (
                    (d := parse_date(item.get("Lot/Serial Number/Expiration Date"))) and d < current_date
                )
                or (
                    (d := parse_date(item.get("Lot/Serial Number/Removal Date"))) and d < current_date
                )
            )
            and (item.get("Available Quantity") not in (0, 0.0, None))
                ]

            
            q_expired_sorted = sorted(
                q_expired,
                key=lambda x: max(
                    d for d in [
                        parse_date(x.get("Lot/Serial Number/Expiration Date")),
                        parse_date(x.get("Lot/Serial Number/Removal Date"))
                    ] if d is not None and d < current_date
                ),
                reverse=True 
                )
            
            # Write expired products report
            f.write(f"\n## Expired/Removed Before Today\n")
            f.write(f"**Total Expired/Removed:** {len(q_expired_sorted)} items\n")

            if q_expired_sorted:
                f.write("| Internal Reference | Product Name | Expiration Date | Removal Date | Available Quantity |\n")
                f.write("|------|--------------|----------------|--------------|------------------|\n")
                for item in q_expired_sorted:
                    sku = item.get("Product/Internal Reference", "N/A")
                    name = item.get("Product/Name", "N/A")
                    exp_date = item.get("Lot/Serial Number/Expiration Date", "N/A")
                    rem_date = item.get("Lot/Serial Number/Removal Date", "N/A")
                    quantity = item.get("Available Quantity", "N/A")
                    f.write(f"| {sku} | {name} | {exp_date} | {rem_date} | {quantity} |\n")
                    
#====================================================================================================            
            q1 = [
            item for item in all_data
            if (
                (
                    (d := parse_date(item.get("Lot/Serial Number/Expiration Date"))) 
                    and current_date <= d <= current_date + timedelta(days=5)
                )
                or (
                    (d := parse_date(item.get("Lot/Serial Number/Removal Date"))) 
                    and current_date <= d <= current_date + timedelta(days=5)
                )
            )
            and (item.get("Available Quantity") not in (0, 0.0, None))
            ]

            # Sort by the earliest future date (expiry or removal)
            q1_sorted = sorted(
                q1,
                key=lambda x: min(
                    d for d in [
                        parse_date(x.get("Lot/Serial Number/Expiration Date")),
                        parse_date(x.get("Lot/Serial Number/Removal Date"))
                    ] if d is not None and d >= current_date
                ),
                reverse=True
            )

            f.write(f"\n## Near expiry/removal During Next 5 days\n")
            f.write(f"**Total of Near expiry/removal within 5 days:** {len(q1_sorted)} items\n")

            if q1_sorted:
                f.write("| Internal Reference | Product Name | Expiration Date | Removal Date | Available Quantity |\n")
                f.write("|------|--------------|----------------|--------------|------------------|\n")
                for item in q1_sorted:
                    sku = item.get("Product/Internal Reference", "N/A")
                    name = item.get("Product/Name", "N/A")
                    exp_date = item.get("Lot/Serial Number/Expiration Date", "N/A")
                    rem_date = item.get("Lot/Serial Number/Removal Date", "N/A")
                    quantity = item.get("Available Quantity", "N/A")
                    f.write(f"| {sku} | {name} | {exp_date} | {rem_date} | {quantity} |\n")
                    
#=============================================================================================
    
            expiry_During_15_day = [
            item for item in all_data
            if (
                (
                    (d := parse_date(item.get("Lot/Serial Number/Expiration Date"))) 
                    and current_date <= d <= current_date + timedelta(days=15)
                )
                or (
                    (d := parse_date(item.get("Lot/Serial Number/Removal Date"))) 
                    and current_date <= d <= current_date + timedelta(days=15)
                )
            )
            and (item.get("Available Quantity") not in (0, 0.0, None))
            ]

            # Sort by the earliest future date (expiry or removal)
            sorted_expiry_During_15_day = sorted(
                expiry_During_15_day,
                key=lambda x: min(
                    d for d in [
                        parse_date(x.get("Lot/Serial Number/Expiration Date")),
                        parse_date(x.get("Lot/Serial Number/Removal Date"))
                    ] if d is not None and d >= current_date
                ),
                reverse=True
            )

            f.write(f"\n## Near expiry/removal During Next 15 days\n")
            f.write(f"**Total of Near expiry/removal within 15 days:** {len(sorted_expiry_During_15_day)} items\n")

            if sorted_expiry_During_15_day:
                f.write("| Internal Reference | Product Name | Expiration Date | Removal Date | Available Quantity |\n")
                f.write("|------|--------------|----------------|--------------|------------------|\n")
                for item in q1_sorted:
                    sku = item.get("Product/Internal Reference", "N/A")
                    name = item.get("Product/Name", "N/A")
                    exp_date = item.get("Lot/Serial Number/Expiration Date", "N/A")
                    rem_date = item.get("Lot/Serial Number/Removal Date", "N/A")
                    quantity = item.get("Available Quantity", "N/A")
                    f.write(f"| {sku} | {name} | {exp_date} | {rem_date} | {quantity} |\n")
                    
#==================================================================================================
        # Q11: Urgent reorder (Available Quantity = 0)
            urgent_reorder = [
                item for item in all_data
                if item.get("Available Quantity") in (0, 0.0, None)
            ]

            sorted_urgent_reorder = sorted(
                urgent_reorder,
                key=lambda x: x.get("Lot/Serial Number/Expiration Date", ""),
                reverse=False
            )

            f.write(f"\n## Urgent Reorder (Out of Stock)\n")
            f.write(f"**Total of Urgent Reorder Items:** {len(sorted_urgent_reorder)} items\n")

            if sorted_urgent_reorder:
                f.write("| Internal Reference | Product Name | Expiration Date | Removal Date | Available Quantity |\n")
                f.write("|------|--------------|--------------|--------------|------------------|\n")
                for item in sorted_urgent_reorder:
                    sku = item.get("Product/Internal Reference", "N/A")
                    name = item.get("Product/Name", "N/A")
                    exp_date = item.get("Lot/Serial Number/Expiration Date", "N/A")
                    rem_date = item.get("Lot/Serial Number/Removal Date", "N/A")
                    quantity = item.get("Available Quantity", "N/A")
                    f.write(f"| {sku} | {name} | {exp_date} | {rem_date} | {quantity} |\n")

#=====================================================================================      
            def Convert_date(date_str):
                """Try parsing date from multiple common formats; return None if it fails."""
                if not date_str:
                    return None
                for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'):
                    try:
                        return datetime.strptime(date_str, fmt)
                    except:
                        pass
                return None

            sku_counts = {}
            for item in all_data:
                sku = item.get("Product/Internal Reference")
                prod_date = Convert_date(item.get("Lot/Serial Number/Expiration Date"))

                if sku:
                    sku_clean = sku.strip().upper()
                    key = (sku_clean, prod_date)
                    sku_counts[key] = sku_counts.get(key, 0) + 1

            dup_skus = {key: count for key, count in sku_counts.items() if count > 1}
            dup_skus_sort = sorted(dup_skus.items(), key=lambda x: x[1], reverse=True)

            top_10_dup_skus = dup_skus_sort[:10]
            f.write("## Top 10 Duplicate SKUs\n")
            f.write("| Internal Reference | Expiration Date | Duplicated |\n")
            f.write("|--------------------|-----------------|------------|\n")
            for (sku, prod_date), count in top_10_dup_skus:
                f.write(f"| {sku} | {prod_date or 'N/A'} | {count} items |\n")


#====================================Final Report ===================================