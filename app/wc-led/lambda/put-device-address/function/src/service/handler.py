from time import sleep
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger
import os
import re
import json

from ..util.exception import ExtendException
from ..helper import dynamodb

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    try:
        logger.info(event)
        print("Received event: " + json.dumps(event))
        # eventの中身をパースする。API Gateway REST APIからのリクエストを想定する。
        if 'httpMethod' in event:
            http_method = event['httpMethod']
            body = event.get('body', '{}')
            if body:
                body = json.loads(body)
            print("body: " + json.dumps(body))
        parse_item = dynamodb.parse_address_put_item(body)
        logger.info(parse_item)
        dynamodb.put_item(parse_item)
    except ClientError as e:
        logger.exception(e)
        return ExtendException(400, 'ClientError, Bad Request.')
    except Exception as e:
        logger.exception(e)
        return ExtendException(400, 'Undefined Error, Bad Request.')

