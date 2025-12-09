from helpers.config import get_settings, Settings
import os
import random 
import string
import tempfile 
from storage import (get_boto3_client, Upload_file_to_s3, download_file_from_s3)
from typing import Optional

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
    
    def generate_random_string(self, length: int = 12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def _get_s3_client(self) -> Optional[object]:
        """Creates and returns the Boto3 S3 client using application settings."""
         
        # Using the imported helper function
        return get_boto3_client(
            s3_url=self.app_settings.ENDPOINT_URL,
            s3_bucket=self.app_settings.AWS_BUCKET,
            s3_region=self.app_settings.REGION,
            s3_access_key=self.app_settings.AWS_ACCESS_KEY_ID,
            s3_secret_key=self.app_settings.AWS_SECRET_ACCESS_KEY
        )
    
    # --- S3 Key Prefix Logic ---
    
    def get_database_key_prefix(self, db_prefix: str) -> str:
        """
        Returns the S3 Key Prefix (e.g., 'database/user_data') for storage.
        """
        return f"database/{db_prefix.strip('/')}"
    
    # --- UPLOAD Method ---
    
    def upload_file_to_s3_only(self, local_file_path: str, s3_key: str) -> str:
        """
        Uploads a file to S3 using a local temporary file path.
        
        :param local_file_path: The full path to the temporary local file to be uploaded.
                                (The caller is responsible for deleting this file.)
        :param s3_key: The full Key (path) where the file will be saved in S3.
        :return: The S3 key the file was saved under.
        """
        s3_client = self._get_s3_client()
        if not s3_client:
            raise ConnectionError("❌ Failed to connect to S3 service.")

        try:
            # Using the imported helper function
            Upload_file_to_s3(
                boto3_client=s3_client,
                file_name=local_file_path,  # Local path
                s3_bucket=self.app_settings.AWS_BUCKET,
                file_path=s3_key            # S3 Key
            )
            print(f"✅ File uploaded successfully to S3 key: {s3_key}")
            return s3_key
        except Exception as e:
            print(f"⚠️ S3 Upload failed for key {s3_key}: {e}")
            raise
    
    # --- DOWNLOAD Method ---
    
    def download_file_from_s3(self, s3_key: str) -> Optional[str]:
        """
        Downloads a file from S3 to a temporary local path.
        
        :param s3_key: The S3 key of the file to download.
        :return: The path to the temporary local file. The caller MUST delete this file.
        """
        s3_client = self._get_s3_client()
        if not s3_client:
            raise ConnectionError("❌ Failed to connect to S3 service.")
        
        # 1. Create a safe temporary directory for the download
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Using the imported helper function
            # Note: We must pass the temporary directory to the helper function
            local_path = download_file_from_s3( 
                boto3_client=s3_client,
                bucket_name=self.app_settings.AWS_BUCKET,
                file_key=s3_key,
                download_directory=temp_dir, # Use the safe temp directory
                # We always force download since the temp dir is new or for temporary use
                force_download=True 
            )
            print(f"✅ File downloaded from S3 to temporary path: {local_path}")
            return local_path
        except Exception as e:
            # Clean up the temp directory if download fails
            if os.path.exists(temp_dir):
                 os.rmdir(temp_dir)
            print(f"⚠️ S3 Download failed for key {s3_key}: {e}")
            return None