import boto3
from aws_lambda_powertools import Logger
import json
import os

logger = Logger(child=True)
# AWS IoTのエンドポイントとデバイス名を設定
IOTENDPOINT = os.environ['IOTENDPOINT']


# AWS IoTクライアントを作成
client = boto3.client('iot-data', endpoint_url=f"https://{IOTENDPOINT}")


def publish(topic: str, payload: dict) -> None:
    """Publish IoT Message
    """
    logger.info(f"Publishing to {topic}")
    logger.info(f"Payload: {json.dumps(payload)}")
    client.publish(
        topic=topic,
        qos=1,
        payload=json.dumps(payload)
    )
    return 