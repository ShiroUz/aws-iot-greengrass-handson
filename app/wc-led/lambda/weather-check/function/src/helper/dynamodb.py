import boto3
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools import Logger
import json
import os
import uuid

from src.util.time import get_utc_time, get_expiration_time

logger = Logger(child=True)
TABLE_NAME = os.environ['TABLE_NAME']
PARTITION_KEY = os.environ['PARTITION_KEY']

# Cold start対策
dynamodb = boto3.resource(
    'dynamodb', region_name=os.environ['REGION'])
table = dynamodb.Table(TABLE_NAME)


def query_partition_key(key: str):
    """Execute query
    I want to refactor logic
    Args:
        key (str): 
    """
    response = table.query(
        KeyConditionExpression=Key(PARTITION_KEY).eq(key)
    )
    query_items = response['Items']
    while 'LastEvaluatedKey' in response: # 最後まで読み込み
        response = table.query(
            KeyConditionExpression=Key(PARTITION_KEY).eq(key),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        query_items.extend(response['Items'])
    
    return query_items

def get_item(partition_key: str):
    """Get Item
    """
    response = table.get_item(
        Key={
            PARTITION_KEY: partition_key,
        }
    )
    return response.get('Item')

def put_item(put_item: dict):
    """Put item
    """
    table.put_item(
        Item=put_item
    )

def put_items(put_items: list):
    """Put items with batch writer

    Args:
        put_params (dict): 
    """
    with table.batch_writer() as batch:
        for put_item in put_items:
            batch.put_item(
                Item=put_item
            )


def delete_all_items():
    """Delete All Items on the table
    I want to refactor code
    """
    item_list = scan()
    pk_list = get_pk_list(item_list)
    with table.batch_writer() as batch:
        for key in pk_list:
            batch.delete_item(Key=key)


def scan() -> list:
    """Scan Table Items
    """
    response = table.scan()
    item_list = response['Items']
    while 'LastEvaluatedKey' in response:
        response = dynamodb.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'])
        item_list.extend(response['Items'])
    return item_list


def get_pk_list(item_list: list) -> list:
    """Get PK [{}] from dynamoDB Items
    """
    return [{PARTITION_KEY: item[PARTITION_KEY]} for item in item_list]


def parse_address_put_item(body: dict) -> dict:
    return {
            PARTITION_KEY: body[PARTITION_KEY],  # partition key
            "UserId": body["UserId"],
            "UserName": body["UserName"],
            "CreateTime": get_utc_time(),
            'Address': body["Address"]
        }
