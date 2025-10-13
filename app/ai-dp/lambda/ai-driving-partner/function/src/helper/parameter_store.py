import boto3
from aws_lambda_powertools import Logger
import json
import os

logger = Logger(child=True)

ssm_client = boto3.client('ssm', region_name=os.environ.get("REGION"))

def get_parameter(parameter_name: str) -> str:
    """Get Parameter Store Value
    """
    response = ssm_client.get_parameter(
        Name=parameter_name,
        WithDecryption=True
    )
    return response['Parameter']['Value']
    