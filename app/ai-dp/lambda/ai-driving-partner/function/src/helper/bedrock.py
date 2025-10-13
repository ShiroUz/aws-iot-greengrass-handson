import boto3
from aws_lambda_powertools import Logger
import json
import os

logger = Logger(child=True)
MAX_TOKENS = 1000

MODEL_ID = os.environ.get("MODEL_ID")
INFERENCE_PROFILE_ARN = os.environ.get("INFERENCE_PROFILE_ARN")
bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name=os.environ.get("REGION"))

def generate_message(prompt, temperature) -> dict:

    body=json.dumps({
      "messages": [
          {
              "role": "user",
              "content": prompt
          }
      ],
    # "messages": [
    #   {
    #     "role": "user",
    #     "content": [
    #       {
    #         "type": "text",
    #         "text": prompt
    #       }
    #     ]
    #   }
    # ],
      "max_tokens": MAX_TOKENS,
      "temperature": temperature,
      "anthropic_version": "bedrock-2023-05-31"
    })
    logger.info(body)
    response = bedrock_runtime.invoke_model(body=body, modelId=MODEL_ID)
    response_body = json.loads(response.get('body').read())
    logger.info(json.dumps(response_body))
    response_text = response_body['content'][0]['text']
   
    return response_text

# Amazon NovaのAPIを利用して、画像とシステムプロンプトを渡して、応答を得る
def generate_message_with_system_prompt_and_image(system_prompt, s3_location, temperature) -> dict:
    user_message = system_prompt
    
    # Extract file extension
    file_extension = s3_location.split('.')[-1].lower()
    
    image = {
        'format': file_extension,
        'source': {
            's3Location': {
                'uri': s3_location
            }
        }
    }
    conversation = [
        {
            'role': 'user',
            'content': [
                {'text': user_message},
                {'image': image}
            ],
        }
    ]
    response = bedrock_runtime.converse(
        modelId=INFERENCE_PROFILE_ARN,
        messages=conversation,
        inferenceConfig={
            'temperature': temperature,
            'maxTokens': MAX_TOKENS,
            "topP": 0.9,
        }
    )
    response_text = response["output"]["message"]["content"][0]["text"]
    return response_text
