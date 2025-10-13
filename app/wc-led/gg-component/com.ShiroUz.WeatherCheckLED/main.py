import sys, os
import logging
from gpiozero import LED, Button
import time
import boto3
import subprocess
from src.helper import s3, iot
from src.util import time as time_util
from src.util import file as file_util

BUCKET_NAME = os.getenv('BUCKET_NAME', "dev-aws-gg-handson-wc-led-tts-xxxxxxxxx")  # S3バケット名を指定
OBJECT_KEY = "communication-test/.ca08c266-c42b-4981-9183-2b989a7ea163.mp3"  # Deploy確認用オブジェクトキー
BASE_FILE_PATH = "/app/audio/"  # ダウンロード後のローカルファイルパス
THING_NAME = os.getenv('AWS_IOT_THING_NAME', "TestDevice")  # IoTデバイスのThing名を環境変数から取得

# PUBLISHトピック名の定義
PUBLISH_WEATHER_CMD_TOPIC_NAME = "cmd/aws_gg_handson/wc_led/{}/weather/req".format(THING_NAME)  # Weather check command topic name

# Subscribeトピック名の定義
SUBSCRIBE_WEATHER_CMD_TOPIC_NAME = "cmd/aws_gg_handson/wc_led/{}/weather/res".format(THING_NAME)  # Weather check response topic name

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WeatherCheckWithDocker")

# GPIOピンの設定
red_led = LED("GPIO27")
yellow_led = LED("GPIO22")
green_led = LED("GPIO23")
umbrella_led = LED("GPIO24")
weather_button = Button("GPIO26")

def get_greeting(name):
    return f"Hello {name}!"

def main():
    args = sys.argv[1:]
    message = " ".join(args) if args else "World"
    greeting = get_greeting(message)
    
    logger.info(greeting)
    logger.info(f"Current time: {time.time()}")
    # LEDの初期化
    red_led.off()
    yellow_led.off()
    green_led.off()
    umbrella_led.off()
    logger.info("LEDs initialized to OFF state")
    # Deploy確認のための音声ファイルを再生
    initial_check()
    
    # LEDを点滅させる
    try:
        logger.info("Starting LED blink sequence in Docker container")
        while True:
            # red_led.on()
            # logger.info("LED RED ON")
            # time.sleep(1)

            # yellow_led.on()
            # logger.info("LED YELLOW ON")
            # time.sleep(1)
            
            # green_led.on()
            # logger.info("LED GREEN ON")
            # time.sleep(1)
            
            # umbrella_led.on()
            # logger.info("Umbrella LED ON")
            # time.sleep(1)
            
            # red_led.off()
            # logger.info("LED RED OFF")
            # time.sleep(1)

            # yellow_led.off()
            # logger.info("LED YELLOW OFF")
            # time.sleep(1)

            # green_led.off()
            # logger.info("LED GREEN OFF")
            # time.sleep(1)

            # 雨傘LEDを点滅させる
            # umbrella_led.off()
            # logger.info("Umbrella LED OFF")
            # time.sleep(1)
            
            # ボタンが押されたらメッセージを表示
            if weather_button.is_pressed:
                logger.info("Button pressed! Weather check initiated.")
                iot_publisher = iot.IoTPublisher()
                payload = { "ThingId": THING_NAME }
                iot_publisher.send_message(PUBLISH_WEATHER_CMD_TOPIC_NAME, payload)
                time.sleep(1)  # ボタンのデバウンス対策

    except KeyboardInterrupt:
        logger.info("Program terminated by user")
    finally:
        red_led.close()
        yellow_led.close()
        green_led.close()
        umbrella_led.close()
        weather_button.close()
        logger.info("GPIO resources released")

# 初期確認
def initial_check():
    logger.info("Starting initial check...")
    # テスト用音声ファイルが存在していたら再生する。
    try:
        file_path = BASE_FILE_PATH + 'deploy-complete-' + str(time_util.get_utc_time()) + ".mp3"
        audio_data = s3.get_object_from_s3(BUCKET_NAME, OBJECT_KEY)
        file_util.save(file_path, audio_data)

        if os.path.exists(file_path):
            subprocess.call(["mpg321", file_path], shell=False)
            logging.info("audio was playeded: %s", file_path)
        else:
            logging.info("audio wasn't played: %s", file_path)
    except Exception as e:
        logging.error("Error during initial check: %s", e)

# トピックのSubscribe
def handle_weather_update(topic, message):
    """
    Handle weather update messages from IoT Core
    """
    logger.info(f"Weather update received on {topic}: {message}")
    # ここで受信したメッセージに基づいて処理を行う
    # 例: LEDの点灯パターンを変更する、音声を再生するなど
    
    try:
        if isinstance(message, dict) and "action" in message:
            # メッセージに基づいて
            logger.info(f"RED LED CHECK: {message['morning']}")
            logger.info(f"RED LED CHECK type: {type(message['morning'])}")
            if message["action"] == "change_led":
                if message["morning"] == 1:
                    red_led.on()
                else:
                    red_led.off()
                logger.info(f"RED LED Update:")
                if message["evening"] == 1:
                    yellow_led.on()
                else:
                    yellow_led.off()
                logger.info(f"YELLOW LED Update:")                      
                if message["night"] == 1:
                    green_led.on()
                else:
                    green_led.off()
                logger.info(f"GREEN LED Update:")
                if message["umbrella"] == 1:
                    umbrella_led.on()
                else:
                    umbrella_led.off()
                logger.info(f"Umbrella LED Update:")

                logger.info(f"LED pattern changed based on message: {message}")
            
            # メッセージに基づいて音声ファイルを再生する
            if message["action"] == "play_sound":
                object_key = message["s3_file_path"]
                audio_data = s3.get_object_from_s3(BUCKET_NAME, object_key)
                file_path = BASE_FILE_PATH + str(time_util.get_utc_time()) + ".mp3"
                file_util.save(file_path, audio_data)        
                if os.path.exists(file_path):
                    subprocess.call(["mpg321", file_path], shell=False)
                    logging.info("audio was playeded: %s", file_path)
    
    except Exception as e:
        logger.error(f"Error processing weather update message: {e}")

def start_subscriber():
    """
    Start the IoT Core subscriber in a separate thread
    """
    try:
        subscriber = iot.IoTSubscriber()
        # 複数のトピックを購読する例
        subscriber.subscribe(SUBSCRIBE_WEATHER_CMD_TOPIC_NAME, handle_weather_update)
        subscriber.subscribe("device/commands")  # デフォルトハンドラーを使用
        
        logger.info("IoT Core subscriber started")
        return subscriber
    except Exception as e:
        logger.error(f"Failed to start IoT Core subscriber: {e}")
        return None

if __name__ == "__main__":
    # サブスクライバーを別スレッドで起動
    subscriber = start_subscriber()
    main()
    
    # プログラム終了時にサブスクライバーをクリーンアップ
    if subscriber:
        subscriber.close()