import boto3
from aws_lambda_powertools import Logger
import json
import os

logger = Logger(child=True)
MAX_TOKENS = 1000

INFERENCE_PROFILE_ARN = os.environ.get("INFERENCE_PROFILE_ARN")
bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name=os.environ.get("REGION"))

def generate_message(prompt, temperature) -> dict:

    conversation = [
        {
            'role': 'user',
            'content': [
                {'text': prompt},
            ],
        }
    ]
    inferenceConfig = {
      "temperature": temperature,
      "topP": 0.9,
      "maxTokens": MAX_TOKENS,
      "stopSequences":[]
    }
    response = bedrock_runtime.converse(
        modelId=INFERENCE_PROFILE_ARN,
        messages=conversation,
        inferenceConfig=inferenceConfig
    )
    response_text = response["output"]["message"]["content"][0]["text"]
    return response_text