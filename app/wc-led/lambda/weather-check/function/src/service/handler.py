from time import sleep
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger
from datetime import datetime
import os
import re
import json

from ..util.exception import ExtendException
from ..util.time import get_utc_time
from ..util.file import save, read
from ..helper import dynamodb, iotcore, s3, bedrock, polly, parameter_store

logger = Logger()

SYSTEMPROMPT_WEATHER_CHECK_NAME = os.environ.get('SYSTEMPROMPT_WEATHER_CHECK_NAME')
SYSTEMPROMPT_TRANSFER_LED_POW_NAME = os.environ.get('SYSTEMPROMPT_TRANSFER_LED_POW_NAME')

PARTITION_KEY = os.environ.get('PARTITION_KEY')
TOPIC = "cmd/aws_gg_handson/wc_led/{}/weather/res"

@logger.inject_lambda_context(log_event=True)
def cron_handler(event, context):
    """
    Event Bridgeからの定期発火にって実行される
    """
    try:
        logger.info(event)
        # 必要なデータを各サービスから持ってくる。
        systemprompt_weather_check = parameter_store.get_parameter(SYSTEMPROMPT_WEATHER_CHECK_NAME)
        systemprompt_transfer_led_pow = parameter_store.get_parameter(SYSTEMPROMPT_TRANSFER_LED_POW_NAME)

        devices_info = dynamodb.scan()
        for device in devices_info:
            # 変更するべき変数の初期化
            weather_check_for_device_prompt = None
            topic = None
            if device.get('Address'):
                address = device['Address']
            # Bedrockで天気予報を確認
            weather_check_for_device_prompt = systemprompt_weather_check + address
            sleep(1)  # BedrockのAPIの制限に引っかからないように、1秒待つ
            today_weather = bedrock.generate_message(weather_check_for_device_prompt, 0.5)
            logger.info(today_weather)
            # 今日の天気をS3に保存
            today_date = datetime.now().strftime('%Y-%m-%d')
            prefix = 'weather/{}/{}'.format(device['ThingId'], today_date)
            key = str(get_utc_time())
            key_file = key + '.txt'
            s3.upload_to_s3(prefix, key_file, today_weather)
            
            # 今日の天気を元に、LEDの明るさを変更
            transfer_led_pow_prompt = systemprompt_transfer_led_pow + today_weather
            sleep(1)  # BedrockのAPIの制限に引っかからないように、1秒待つ
            transfer_led_pow = bedrock.generate_message(transfer_led_pow_prompt, 1)
            # Bedrockからの応答によっては、json形式ではない場合がある。プロンプトの問題
            logger.info(type(transfer_led_pow))
            logger.info(transfer_led_pow)
            led_pow_data = json.loads(transfer_led_pow)
            # LEDの明るさを変更
            topic = TOPIC.format(device['ThingId'])
            led_pow_data['action'] = 'change_led'
            iotcore.publish(topic, led_pow_data)

    except ClientError as e:
        logger.exception(e)
        return ExtendException(400, 'ClientError, Bad Request.')
    except Exception as e:
        logger.exception(e)
        return ExtendException(400, 'Undefined Error, Bad Request.')


@logger.inject_lambda_context(log_event=True)
def event_handler(event, context):
    """
    IoT CoreのRuleから実行されるhandler
    """
    try:
        logger.info(event)
        logger.info(SYSTEMPROMPT_WEATHER_CHECK_NAME)
        # 必要なデータを各サービスから持ってくる。
        systemprompt_weather_check = parameter_store.get_parameter(SYSTEMPROMPT_WEATHER_CHECK_NAME)
        systemprompt_transfer_led_pow = parameter_store.get_parameter(SYSTEMPROMPT_TRANSFER_LED_POW_NAME)
        
        device_info = dynamodb.get_item(event['ThingId'])
        address = device_info['Address']
        # Bedrockで天気予報を確認
        weather_check_for_device_prompt = systemprompt_weather_check + address
        sleep(1)  # BedrockのAPIの制限に引っかからないように、1秒待つ
        today_weather = bedrock.generate_message(weather_check_for_device_prompt, 0.5)
        logger.info(today_weather)
        # 今日の天気をS3に保存
        today_date = datetime.now().strftime('%Y-%m-%d')
        prefix = 'weather/{}/{}'.format(device_info['ThingId'], today_date)
        key = str(get_utc_time())
        key_txt_file = key + '.txt'
        s3.upload_to_s3(prefix, key_txt_file, today_weather)

        # 定期実行の時との差分
        # ttsファイルを作成し、payloadの中に、参照するべきファイルを一緒に送るようにする。
        speach_data = polly.generate_audio(today_weather.replace('\n', ''))
        key_tts_file = key + '.mp3'
        tmp_save_path = save(key_tts_file, speach_data)
        s3.upload_mp3_to_s3(prefix, key_tts_file, tmp_save_path)
        
        # 今日の天気を元に、LEDの明るさを変更
        transfer_led_pow_prompt = systemprompt_transfer_led_pow + today_weather
        sleep(1)  # BedrockのAPIの制限に引っかからないように、1秒待つ
        transfer_led_pow = bedrock.generate_message(transfer_led_pow_prompt, 1)
        logger.info(json.loads(transfer_led_pow))
        led_pow_data = json.loads(transfer_led_pow)
        led_pow_data['s3_file_path'] = f"{prefix}/{key_tts_file}"
        logger.info(led_pow_data)
        # LEDの明るさを変更
        topic = TOPIC.format(device_info['ThingId'])
        led_pow_data['action'] = 'change_led'
        iotcore.publish(topic, led_pow_data)

        led_pow_data['action'] = 'play_sound'
        iotcore.publish(topic, led_pow_data)

    except ClientError as e:
        logger.exception(e)
        return ExtendException(400, 'ClientError, Bad Request.')
    except Exception as e:
        logger.exception(e)
        return ExtendException(400, 'Undefined Error, Bad Request.')
