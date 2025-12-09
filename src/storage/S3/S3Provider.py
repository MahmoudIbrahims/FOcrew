from typing import Optional
from boto3 import client
import os
from pathlib import Path

def get_boto3_client(
    s3_url: str,
    s3_bucket: str,
    s3_region: str,
    s3_access_key: str,
    s3_secret_key: str
) -> Optional[object]:
    
    return client(
        's3',
        endpoint_url=s3_url,
        region_name=s3_region,
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key
    )


def Upload_file_to_s3(
      boto3_client:object,
      file_name:str,
      s3_bucket:str,
      file_path:str,
      
) -> bool:

   boto3_client.upload_file(
                        Filename=file_name,
                        Bucket=s3_bucket,
                        Key=file_path.replace(f"{s3_bucket}/", "").strip()
                    )
   
   return f"success the Upload in{s3_bucket}"

def download_file_from_s3(
    boto3_client: object,
    bucket_name: str,
    file_key: str,
    download_directory: str,
    force_download: bool = False
) -> bool:
    
    # create local dir to download the file
    download_path = os.path.join(
        download_directory,
        os.path.basename(file_key)
    )

       # create local dir to download the file
    download_path = os.path.join(
        download_directory,
        os.path.basename(file_key)
    )

    if os.path.exists(download_path) and not force_download:
        return download_path
    
    boto3_client.download_file(
                        bucket_name,
                        file_key,
                        download_path
                        )

    return download_path