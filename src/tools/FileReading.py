from crewai_tools import FileReadTool,DirectoryReadTool
from .Schema import BatchFileReaderSchema
from crewai.tools import BaseTool
from pydantic import BaseModel
import dask.dataframe as dd
from typing import Type
import dask.dataframe as dd
import pandas as pd
import time
import json
import os
import logging
import psutil 



logging.basicConfig(filename='batch_reader.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s')


def FileTool():
    file_tool = FileReadTool()
    return file_tool
    
def DirectoryTool():
    directory_tool = DirectoryReadTool()
    return directory_tool



class BatchFileReader(BaseTool):
    name: str = "Batch File Reader"
    description: str = "Reads CSV or Excel files in batches optimized for Gemini's context length."
    args_schema: Type[BaseModel] = BatchFileReaderSchema

    def _estimate_tokens(self, data: list) -> int:
        """Estimate the number of tokens in a batch for Gemini."""
        try:
            cleaned_data = self._clean_batch_data(data)  # Clean data before estimating tokens
            text = json.dumps(cleaned_data, ensure_ascii=False)
            words = len(text.split())
            chars = len(text)
            estimated_tokens = max(1, words + (chars // 6))  # Ensure at least 1 token
            logging.info(f"Estimated tokens for batch: {estimated_tokens}")
            # Log memory usage
            memory_info = psutil.Process().memory_info()
            logging.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
            return estimated_tokens
        except Exception as e:
            logging.error(f"Error estimating tokens: {str(e)}")
            raise

    def _clean_batch_data(self, batch_data: list) -> list:
        """Convert Timestamp objects and non-serializable types to strings."""
        cleaned_data = []
        for record in batch_data:
            cleaned_record = {}
            for key, value in record.items():
                if isinstance(value, pd.Timestamp):
                    cleaned_record[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                elif pd.isna(value):
                    cleaned_record[key] = ""
                else:
                    cleaned_record[key] = value
            cleaned_data.append(cleaned_record)
        return cleaned_data

    def _save_batch(self, batch_data: list, batch_index: int):
        """Save batch to a temporary JSON file."""
        try:
            os.makedirs("temp_batches", exist_ok=True)
            batch_file = f"temp_batches/batch_{batch_index}.json"
            batch_data = self._clean_batch_data(batch_data)
            with open(batch_file, "w", encoding="utf-8") as f:
                json.dump(batch_data, f, ensure_ascii=False)
            logging.info(f"Saved batch {batch_index} to {batch_file}")
            return batch_file
        except Exception as e:
            logging.error(f"Error saving batch {batch_index}: {str(e)}")
            raise

    def _run(self, file_path: str, num_batches: int = 20, sleep_time: int = 5, mime_type: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", max_tokens_per_batch: int = 500):
        try:
            logging.info(f"Starting to process file: {file_path}")
            result = []
            if mime_type == "text/csv":
                logging.info("Reading CSV file")
                ddf = dd.read_csv(file_path, usecols=lambda col: col not in ["Lot/Serial Number", "Product/Breadfast Barcode"])
                total_rows = len(ddf)
                logging.info(f"Total rows in CSV: {total_rows}")
                batch_size = max(1, total_rows // num_batches)
                
                for i in range(0, total_rows, batch_size):
                    logging.info(f"Processing batch {len(result)} from rows {i} to {i + batch_size}")
                    chunk = ddf[i:i + batch_size].compute()
                    batch_data = chunk.to_dict(orient="records")
                    while self._estimate_tokens(batch_data) > max_tokens_per_batch:
                        logging.warning(f"Batch size too large ({self._estimate_tokens(batch_data)} tokens), reducing batch size")
                        batch_size = max(1, batch_size // 2)
                        batch_data = batch_data[:batch_size]
                    batch_file = self._save_batch(batch_data, len(result))
                    result.append(batch_file)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
            elif mime_type in [
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ]:
                logging.info("Reading Excel file")
                df = pd.read_excel(file_path, engine="openpyxl")
                df = df.drop(columns=["Lot/Serial Number", "Product/Breadfast Barcode"], errors="ignore")
                total_rows = df.shape[0]
                logging.info(f"Total rows in Excel: {total_rows}")
                batch_size = max(1, total_rows // num_batches)
                for i in range(0, total_rows, batch_size):
                    logging.info(f"Processing batch {len(result)} from rows {i} to {i + batch_size}")
                    chunk = df.iloc[i:i + batch_size]
                    batch_data = chunk.to_dict(orient="records")
                    while self._estimate_tokens(batch_data) > max_tokens_per_batch:
                        logging.warning(f"Batch size too large ({self._estimate_tokens(batch_data)} tokens), reducing batch size")
                        batch_size = max(1, batch_size // 2)
                        batch_data = batch_data[:batch_size]
                    batch_file = self._save_batch(batch_data, len(result))
                    result.append(batch_file)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
            else:
                logging.error(f"Unsupported MIME type: {mime_type}")
                return f"Unsupported MIME type: {mime_type}"
            logging.info(f"Completed processing, generated {len(result)} batches")
            return result
        except Exception as e:
            logging.error(f"Error processing file: {str(e)}")
            import traceback
            return f"Error processing file: {str(e)}\n{traceback.format_exc()}"