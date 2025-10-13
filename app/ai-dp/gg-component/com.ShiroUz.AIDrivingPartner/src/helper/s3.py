import boto3
from typing import Any, Dict
import os
import logging

logger = logging.getLogger("S3Helper")

s3_client = boto3.client('s3', region_name=os.getenv('AWS_REGION', 'ap-northeast-1'))

def get_object_from_s3(bucket_name: str, full_key: str) -> Any:
    """Get object from S3"""
    try:
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=full_key
        )
        return response['Body'].read()
    except Exception as e:
        logger.error(f"Failed to get object from S3: {str(e)}")
        raise

def download_file(bucket_name: str, object_key: str, local_file_path: str):
    """Download a file from S3 to local storage"""
    try:
        s3_client.download_file(bucket_name, object_key, local_file_path)
        logger.info(f"Successfully downloaded file from S3: {bucket_name}/{object_key} to {local_file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to download file from S3: {str(e)}")
        return False

def upload_file(local_file_path: str, bucket_name: str, object_key: str):
    """Upload a file to S3 from local storage"""
    try:
        s3_client.upload_file(local_file_path, bucket_name, object_key)
        logger.info(f"Successfully uploaded file to S3: {local_file_path} to {bucket_name}/{object_key}")
        return True
    except Exception as e:
        logger.error(f"Failed to upload file to S3: {str(e)}")
        return False

def delete_file(bucket_name: str, object_key: str):
    """Delete a file from S3"""
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        logger.info(f"Successfully deleted file from S3: {bucket_name}/{object_key}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete file from S3: {str(e)}")
        return False