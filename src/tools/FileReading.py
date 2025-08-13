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
from pathlib import Path


logging.basicConfig(filename='batch_reader.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s')



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
    
    # def _check_existing_batches(self, output_directory:str ,cache_key: str) -> list:
    #     """check existing"""
    #     cache_dir = f"temp_batches/{cache_key}"
    #     if not os.path.exists(cache_dir):
    #         return []
    

    def _check_existing_batches(self, output_directory: str, cache_key: str) -> list:
        """Check existing"""
        cache_dir = Path(output_directory) / cache_key
        if not cache_dir.exists():
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

    def _save_batch(self, batch_data: list, batch_index: int, cache_key: str,output_directory: str):
        """save batch"""
        try:
            # cache_dir = f"temp_batches/{cache_key}"
            cache_dir = Path(output_directory) / cache_key
            os.makedirs(cache_dir, exist_ok=True)
            batch_file = f"{cache_dir}/batch_{batch_index}.json"
            
            cleaned_data = self._clean_batch_data(batch_data)
            with open(batch_file, "w", encoding="utf-8") as f:
                json.dump(cleaned_data, f, ensure_ascii=False, separators=(',', ':'))
            
            return batch_file
        except Exception as e:
            logging.error(f"Error saving batch {batch_index}: {str(e)}")
            raise

    def _run(self, file_path: str, num_batches: int = 50, sleep_time: int = 0, 
             mime_type: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
             max_tokens_per_batch: int = 10000,output_directory: str="results/Mini_Batches"):  
        try:
            cache_key = self._get_cache_key(file_path)
            logging.info(f"Processing file: {file_path} with cache key: {cache_key}")
            
            if not os.path.exists(output_directory):
                os.makedirs(output_directory, exist_ok=True)
            
            existing_batches = self._check_existing_batches(output_directory,cache_key)
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
                batch_file = self._save_batch(batch, i, cache_key,output_directory)
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

