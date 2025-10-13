import boto3
from typing import Any, Dict
import os

s3_client = boto3.client('s3',region_name=os.getenv('REGION', 'ap-northeast-1'))

def get_object_from_s3(bucket_name: str,full_key: str) -> Any:
    """Get object from S3
    """
    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=full_key
    )
    return response['Body'].read()

def download_file(bucket_name, object_key, local_file_path):
    s3_client.download_file(bucket_name, object_key, local_file_path)
