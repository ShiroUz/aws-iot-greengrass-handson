import sys, os
import logging
import time
import cv2
import boto3
import subprocess
import json
import threading
import queue
from src.helper import s3, iot
from src.util import time as time_util
from src.util import file as file_util
from src.util.optical_flow import OpticalFlowAnalyzer
from src.util.network import get_local_ip
from src.server.streaming_server import start_server, stop_server, update_latest_frame

# Configuration
BUCKET_NAME = os.getenv('S3_BUCKET_NAME', "dev-aws-gg-handson-ai-dp-content-xxxxxxxxxxx")  # S3 bucket for near-miss images
IMAGES_DIR = os.getenv('IMAGES_DIR', "/app/images/")  # Directory for storing images
AUDIO_DIR = os.getenv('AUDIO_DIR', "/app/audio/")  # Directory for storing audio feedback
THING_NAME = os.getenv('AWS_IOT_THING_NAME', "TestDevice")  # IoT device Thing name
REGION = os.getenv('AWS_REGION', 'ap-northeast-1')  # AWS region
NEAR_MISS_THRESHOLD = int(float(os.getenv('OpticalFlowThreshold', 150000)))  # Threshold for near-miss detection (adjusted for 1/4 size)
CAPTURE_INTERVAL = int(float(os.getenv('CaptureInterval', 2)))  # Sleep interval between image captures
WEB_SERVER_PORT = int(float(os.getenv('WEB_SERVER_PORT', 8080)))  # Web server port for image streaming

# Topic definitions
SUBSCRIBE_FEEDBACK_TOPIC = f"cmd/aws_gg_handson/ai_dp/{THING_NAME}/near-miss/feedback"

# Create directories if they don't exist
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AIDrivingPartner")

# Debug: Print all environment variables related to configuration
logger.info(f"S3_BUCKET_NAME env var: '{os.getenv('S3_BUCKET_NAME')}'")
logger.info(f"IMAGE_DIR env var: '{os.getenv('IMAGES_DIR')}'")
logger.info(f"AUDIO_DIR env var: '{os.getenv('AUDIO_DIR')}'")
logger.info(f"OpticalFlowThreshold env var: '{os.getenv('OpticalFlowThreshold')}'")
logger.info(f"CaptureInterval env var: '{os.getenv('CaptureInterval')}'")
logger.info(f"Final BUCKET_NAME: '{BUCKET_NAME}'")
logger.info("All environment variables:")
for key, value in os.environ.items():
    if 'S3' in key or 'BUCKET' in key:
        logger.info(f"  {key}={value}")

# Global variables
feedback_queue = queue.Queue()
current_state = {
    "near_miss_detected": False,
    "feedback_pending": False,
    "is_stable": True
}
image_server = None  # HTTP server for image streaming

# Initialize the optical flow analyzer with adjusted threshold for 1/4 size frames
analyzer = OpticalFlowAnalyzer(threshold=NEAR_MISS_THRESHOLD)  # Adjusted threshold for resized frames

def capture_frame():
    """Capture a frame from the camera"""
    try:
        # Try different backends for Raspberry Pi
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Use V4L2 backend
        if not cap.isOpened():
            logger.warning("V4L2 backend failed, trying default")
            cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Failed to open camera with any backend")
            return None
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            logger.error("Failed to capture frame")
            return None
        
        return frame
    except Exception as e:
        logger.error(f"Error capturing frame: {str(e)}")
        return None

def process_frame(frame):
    """Convert frame to grayscale and resize to 1/4"""
    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Resize to 1/4 (half width and half height)
    height, width = gray_frame.shape
    new_width = width // 2
    new_height = height // 2
    resized_frame = cv2.resize(gray_frame, (new_width, new_height))
    
    return resized_frame

def save_frame(frame, is_near_miss=False):
    """Save frame to disk and optionally upload to S3"""
    try:
        timestamp = time_util.get_utc_time()
        timestamp_str = str(timestamp)
        local_path = os.path.join(IMAGES_DIR, timestamp_str, f"frame_{timestamp_str}.jpg")
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        cv2.imwrite(local_path, frame)
        logger.debug(f"Frame saved to {local_path}")
        
        # Upload to S3 if it's a near-miss incident
        if is_near_miss:
            object_key = f"near-miss/{THING_NAME}/{timestamp_str}/frame_{timestamp_str}.jpg"
            s3.upload_file(local_path, BUCKET_NAME, object_key)
            logger.info(f"Near-miss frame uploaded to S3: {object_key}")
            return local_path, object_key
        
        return local_path, None
    except Exception as e:
        logger.error(f"Error saving frame: {str(e)}")
        return None, None

def handle_near_miss(frame, object_key):
    """Handle a near-miss incident - update state only, no publishing"""
    try:
        logger.info(f"Near-miss incident handled. Image uploaded to S3: {BUCKET_NAME}/{object_key}")
        
        # Update state
        current_state["near_miss_detected"] = True
        current_state["feedback_pending"] = True
    except Exception as e:
        logger.error(f"Error handling near-miss incident: {str(e)}")

def handle_feedback(topic, message):
    """
    Handle feedback messages from IoT Core
    """
    try:
        logger.info(f"Feedback received: {message}")
        
        if isinstance(message, dict) and "audio_key" in message:
            # Add to feedback queue for processing when stable
            feedback_queue.put(message)
            logger.info("Feedback added to queue for processing when driving is stable")
    except Exception as e:
        logger.error(f"Error processing feedback message: {str(e)}")

def process_feedback():
    """Process feedback from the queue when driving is stable"""
    while True:
        try:
            if current_state["is_stable"] and not feedback_queue.empty():
                message = feedback_queue.get()
                
                # Download and play audio feedback
                logger.info(f"Processing feedback: {message}")
                
                # Download audio file from S3
                bucket = message.get("bucket", BUCKET_NAME)
                audio_key = message.get("audio_key")
                local_file_path = os.path.join(AUDIO_DIR, f"feedback_{time_util.get_utc_time()}.mp3")
                
                if s3.download_file(bucket, audio_key, local_file_path):
                    # Play audio feedback
                    logger.info(f"Playing audio feedback: {local_file_path}")
                    subprocess.call(["mpg321", local_file_path], shell=False)
                    
                    # Delete the near-miss image if requested
                    if "image_key" in message and message.get("delete_image", True):
                        s3.delete_file(bucket, message["image_key"])
                        logger.info(f"Deleted near-miss image: {message['image_key']}")
                
                # Reset state
                current_state["feedback_pending"] = False
                
                # Mark task as done
                feedback_queue.task_done()
                
            # Sleep to avoid busy waiting
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"Error processing feedback: {str(e)}")
            time.sleep(CAPTURE_INTERVAL)  # Wait before retrying

def start_subscriber():
    """Start the IoT Core subscriber"""
    try:
        subscriber = iot.IoTSubscriber()
        subscriber.subscribe(SUBSCRIBE_FEEDBACK_TOPIC, handle_feedback)
        logger.info(f"Subscribed to topic: {SUBSCRIBE_FEEDBACK_TOPIC}")
        return subscriber
    except Exception as e:
        logger.error(f"Failed to start IoT Core subscriber: {str(e)}")
        return None

def main():
    logger.info("AI Driving Partner started")
    
    # Start the feedback processor in a separate thread
    feedback_thread = threading.Thread(target=process_feedback, daemon=True)
    feedback_thread.start()
    
    # Start IoT subscriber
    subscriber = start_subscriber()
    if not subscriber:
        logger.error("Failed to start subscriber. Exiting.")
        return
        
    # Start the image streaming server
    global image_server
    local_ip = get_local_ip()
    image_server = start_server(host=local_ip, port=WEB_SERVER_PORT, images_dir=IMAGES_DIR)
    if image_server:
        logger.info(f"Image streaming server started at http://{local_ip}:{WEB_SERVER_PORT}")
        logger.info(f"Access the image viewer at http://{local_ip}:{WEB_SERVER_PORT}/")
    else:
        logger.warning("Failed to start image streaming server")
    
    try:
        # Main loop
        while True:
            # Capture frame
            raw_frame = capture_frame()
            if raw_frame is None:
                time.sleep(1)
                continue
            
            # Process frame (grayscale + resize to 1/4)
            processed_frame = process_frame(raw_frame)
            
            # Update latest frame for streaming (use processed frame)
            # Convert back to BGR for streaming
            streaming_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
            update_latest_frame(streaming_frame)
            
            # Analyze frame with optical flow using processed frame
            is_near_miss, is_stable, flow_magnitude, frame_with_flow = analyzer.analyze_frame(processed_frame)
            
            # Update current state
            current_state["is_stable"] = is_stable
            
            # Log status with more detail
            logger.info(f"Flow: {flow_magnitude:.2f}, Near miss: {is_near_miss}, Stable: {is_stable}, Threshold: {analyzer.threshold}")
            
            # Handle near-miss incident
            if is_near_miss and not current_state["near_miss_detected"]:
                logger.info("Near-miss incident detected!")
                # Convert grayscale flow frame back to BGR for saving
                if len(frame_with_flow.shape) == 2:  # If grayscale
                    save_frame_bgr = cv2.cvtColor(frame_with_flow, cv2.COLOR_GRAY2BGR)
                else:
                    save_frame_bgr = frame_with_flow
                local_path, object_key = save_frame(save_frame_bgr, is_near_miss=True)
                if object_key:
                    handle_near_miss(processed_frame, object_key)
                # Reset flags to detect new incidents
                analyzer.reset_near_miss_flag()
                
            # Reset near-miss state when driving becomes stable
            if is_stable and current_state["near_miss_detected"]:
                logger.info("Driving stabilized - resetting near-miss detection")
                current_state["near_miss_detected"] = False
            
            # Wait for the configured interval
            time.sleep(1)  # Capture every 1 second for better responsiveness
            
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
    finally:
        if subscriber:
            subscriber.close()
        if image_server:
            stop_server(image_server)
            logger.info("Image streaming server stopped")
        logger.info("AI Driving Partner shutting down")

if __name__ == "__main__":
    main()