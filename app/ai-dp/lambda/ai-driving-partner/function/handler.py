from time import sleep
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger
from datetime import datetime
import os
import re
import json

from src.util.exception import ExtendException
from src.util.time import get_utc_time, unix_to_utc_string
from src.util.file import save, read
from src.helper import dynamodb, iotcore, s3, bedrock, polly, parameter_store

logger = Logger()

SYSTEMPROMPT_NEAR_MISS_FEEDBACK = os.environ.get('SYSTEMPROMPT_NEAR_MISS_FEEDBACK')

PARTITION_KEY = os.environ.get('PARTITION_KEY')
RANGE_KEY = os.environ.get('RANGE_KEY')
TOPIC = "cmd/aws_gg_handson/ai_dp/{}/near-miss/feedback"

@logger.inject_lambda_context(log_event=True)
def event_handler(event, context):
    """
    IoT CoreのRuleから実行されるhandler
    """
    try:
        # https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/userguide/ev-events.html
        logger.info(event)
        # 必要なデータを各サービスから持ってくる。
        systemprompt_near_miss_feedback = parameter_store.get_parameter(SYSTEMPROMPT_NEAR_MISS_FEEDBACK)
        
        # 1. EventBridgeトリガーから利用するS3のバケット名とオブジェクトキーを取得
        bucket_name = event['detail']['bucket']['name']
        object_key = event['detail']['object']['key']
        logger.info(f"Bucket: {bucket_name}, Key: {object_key}")

        # 2. EventBridgeトリガーから、timestampとThingIdを取得
        timestamp = event['detail']['object']['key'].split('/')[2]
        thing_id = event['detail']['object']['key'].split('/')[1]
        logger.info(f"Timestamp: {timestamp}, ThingId: {thing_id}")
        
        
        # 重複処理防止: DynamoDBで既に処理済みかチェック
        existing_item = dynamodb.get_item_by_keys(thing_id, int(timestamp))
        if existing_item:
            logger.info(f"Item already processed: {thing_id}/{timestamp}")
            return {"statusCode": 200, "body": "Already processed"}
        
        # 3. .jpgファイルの場合は.jpegとして再保存
        if object_key.endswith('.jpg'):
            # .jpegとして再保存
            jpeg_object_key = object_key.replace('.jpg', '.jpeg')
            s3.copy_file_with_new_extension(bucket_name, object_key, jpeg_object_key)
            
            # Bedrock用のS3 URIを更新
            s3_uri = f"s3://{bucket_name}/{jpeg_object_key}"
        else:
            s3_uri = f"s3://{bucket_name}/{object_key}"
        
        # Amazon Novaを利用し、Feedbackを生成する
        feedback = bedrock.generate_message_with_system_prompt_and_image(systemprompt_near_miss_feedback, s3_uri, 0.9)
        logger.info(f"Feedback: {feedback}")

        # 4. Feedbackを音声データとして生成し、S3に保存する
        speach_data = polly.generate_audio(feedback.replace('\n', ''))
        key_tts_file = timestamp + '-feedback_audio.mp3'
        tmp_save_path = save(key_tts_file, speach_data)
        s3.upload_mp3_to_s3(os.path.dirname(object_key), key_tts_file, tmp_save_path)
        logger.info("S3 Feedback Audio Upload Success")

        # 5.DynamoDBにFeedbackを保存する。
        # 保存情報は、ThingId, Timestamp, FeedbackText, FeedbackAudioS3Uri, NearMissImageS3Uri
        feedback_audio_s3_key = f"{os.path.dirname(object_key)}/{key_tts_file}"
        # .jpegファイルが作成された場合はそちらを記録
        image_s3_key = jpeg_object_key if object_key.endswith('.jpg') else object_key
        dynamodb.put_item({
            PARTITION_KEY: thing_id,
            RANGE_KEY: int(timestamp),
            'FeedbackText': feedback,
            'FeedbackAudioS3Key': feedback_audio_s3_key,
            'NearMissImageS3Key': image_s3_key,
            'ProcessedAt': get_utc_time(),
            'ExpirationTime': get_utc_time() + 60 * 60 * 24 * 7  # 7日後に自動削除
        })
        logger.info("DynamoDB Store Event Success")

        # 6. IoT CoreにFeedbackを送信する。
        # 送信する情報は、ThingId, FeedbackAudioS3Key, Bucket
        topic = TOPIC.format(thing_id)
        payload = {
            'audio_key': feedback_audio_s3_key, 
            'bucket': bucket_name
        }
        iotcore.publish(topic, payload)
        logger.info("IoT Core Publish Success")

    except ClientError as e:
        logger.exception(e)
        return ExtendException(400, 'ClientError, Bad Request.')
    except Exception as e:
        logger.exception(e)
        return ExtendException(400, 'Undefined Error, Bad Request.')
