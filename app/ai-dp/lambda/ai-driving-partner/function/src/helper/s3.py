import boto3
from aws_lambda_powertools import Logger
import json
import os
from typing import Any, Dict
logger = Logger(child=True)

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
REGION = os.environ.get("REGION")

s3_client = boto3.client('s3',region_name=REGION)

def upload_to_s3(prefix: str, key: str, data: Any) -> Dict[str, str]:
    """Upload data to S3
    """
    full_key = f"{prefix.rstrip('/')}/{key}"
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=full_key,
        Body=data
    )
    return {
      "status": "success",
      "location": f"s3://{S3_BUCKET_NAME}/{full_key}"
    }

def upload_mp3_to_s3(prefix: str, key: str, file_name: str) -> Dict[str, str]:
    """Upload data to S3
    """
    full_key = f"{prefix.rstrip('/')}/{key}"
    with open(file_name, 'rb') as data:    
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=full_key,
            Body=data,
            # ContentType='audio/mpeg'
            ContentType='audio/wav'
        )
    return {
      "status": "success",
      "location": f"s3://{S3_BUCKET_NAME}/{full_key}"
    }

def get_object_from_s3(prefix: str, key: str) -> Any:
    """Get object from S3
    """
    full_key = f"{prefix.rstrip('/')}/{key}"
    response = s3_client.get_object(
        Bucket=S3_BUCKET_NAME,
        Key=full_key
    )
    return response['Body'].read()

def download_file_as_bytes(bucket: str, key: str) -> bytes:
    """Download file from S3 as bytes
    """
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response['Body'].read()

def copy_file_with_new_extension(bucket: str, source_key: str, dest_key: str):
    """Copy S3 file with new extension
    """
    s3_client.copy_object(
        Bucket=bucket,
        CopySource={'Bucket': bucket, 'Key': source_key},
        Key=dest_key
    )