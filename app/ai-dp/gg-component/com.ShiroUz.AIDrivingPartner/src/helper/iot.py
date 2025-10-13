import boto3
import json
import os
import traceback

import awsiot.greengrasscoreipc.clientv2 as clientV2
import awsiot.greengrasscoreipc.model as model
import json
import logging

class IoTPublisher:
    def __init__(self):
        self.logger = logging.getLogger("IoTPublisher")
        self.logger.info("Connecting to Greengrass Core")
        self.ipc_client = clientV2.GreengrassCoreIPCClientV2()
        self.logger.info("Connection complete!")

    def send_message(self, topic:str, payload: any):
        resp = self.ipc_client.publish_to_iot_core(
            topic_name=topic,
            qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(payload).encode()
        )

        try:
            self.ipc_client.close()
            self.logger.info("Message published successfully to topic: %s", topic)
            self.logger.debug("Payload: %s", json.dumps(payload))
            self.logger.info("Closing IPC client connection and successfully published message")
        except Exception as e:
            self.logger.error("Failed to publish message:", e)
    

class IoTSubscriber:
    def __init__(self):
        self.logger = logging.getLogger("IoTSubscriber")
        self.logger.info("Connecting to Greengrass Core")
        self.ipc_client = clientV2.GreengrassCoreIPCClientV2()
        self.logger.info("Connection complete!")
        self.subscriptions = {}
        self.handlers = {}

    def subscribe(self, topic, callback=None):
        """
        Subscribe to an IoT Core topic
        
        Args:
            topic (str): The topic to subscribe to
            callback (callable, optional): Function to call when message is received.
                                          Should accept topic_name and message parameters.
        """
        self.logger.info(f"Subscribing to topic: {topic}")
        
        # Store callback if provided
        if callback:
            self.handlers[topic] = callback
            
        # Subscribe to the topic
        subscription = self.ipc_client.subscribe_to_iot_core(
            topic_name=topic,
            qos=model.QOS.AT_LEAST_ONCE, 
            on_stream_event=self._on_stream_event,
            on_stream_error=self._on_stream_error,
            on_stream_closed=self._on_stream_closed
        )
        
        # Store subscription for later management
        self.subscriptions[topic] = subscription
        return subscription

    def unsubscribe(self, topic):
        """Unsubscribe from a topic"""
        if topic in self.subscriptions:
            self.logger.info(f"Unsubscribing from topic: {topic}")
            self.subscriptions[topic].close()
            del self.subscriptions[topic]
            if topic in self.handlers:
                del self.handlers[topic]
            return True
        return False
    
    def _on_stream_event(self, event):
        try:
            topic_name = event.message.topic_name
            message = str(event.message.payload, 'utf-8')
            
            # Try to parse as JSON
            try:
                message_data = json.loads(message)
            except json.JSONDecodeError:
                message_data = message
                
            self.logger.debug(f'Received message on topic {topic_name}: {message}')
            
            # Call specific handler if registered
            if topic_name in self.handlers and callable(self.handlers[topic_name]):
                self.handlers[topic_name](topic_name, message_data)
            else:
                # Default handling
                self.logger.info(f'Message on topic {topic_name}: {message}')
                
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            traceback.print_exc()

    def _on_stream_error(self, error):
        self.logger.error(f"Stream error: {error}")
        # Return True to close stream, False to keep stream open.
        return True  

    def _on_stream_closed(self):
        self.logger.info("Stream closed")
        
    def close(self):
        """Close all subscriptions and the IPC client"""
        for topic in list(self.subscriptions.keys()):
            self.unsubscribe(topic)
        try:
            self.ipc_client.close()
            self.logger.info("Closed IPC client connection")
        except Exception as e:
            self.logger.error(f"Failed to close IPC client: {str(e)}")