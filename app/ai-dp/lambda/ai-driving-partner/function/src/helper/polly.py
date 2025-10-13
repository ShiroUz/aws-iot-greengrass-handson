import boto3
from aws_lambda_powertools import Logger
import json
import os

logger = Logger(child=True)

TTS_MODEL = os.environ.get("TTS_MODEL")
REGION = os.environ.get("REGION")

polly = boto3.client('polly', region_name=os.environ.get("REGION"))

def generate_audio(text: str) -> bytes:
    """Generate audio from text
    """
    response = polly.synthesize_speech(
        Engine='neural',
        Text=text,
        OutputFormat='mp3',
        # OutputFormat='wav',
        VoiceId=TTS_MODEL
    )
    return response['AudioStream'].read()