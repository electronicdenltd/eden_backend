import time
import paho.mqtt.client as paho
from paho import mqtt


class MQTTClient:
    def __init__(self, broker, port, username, password, client_id=""):
        """
        Initialize MQTT Client
        
        Args:
            broker: MQTT broker address
            port: MQTT broker port
            username: Username for authentication
            password: Password for authentication
            client_id: Client ID (optional)
        """
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        
        # Create client
        self.client = paho.Client(client_id=client_id, userdata=None, protocol=paho.MQTTv5)
        
        # Set callbacks
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        
        # Configure TLS and authentication
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(self.username, self.password)
    
    def on_connect(self, client, userdata, flags, rc, properties=None):
        """Callback when connection is established"""
        print("CONNACK received with code %s." % rc)
    
    def on_publish(self, client, userdata, mid, properties=None):
        """Callback when message is published"""
        print("mid: " + str(mid))
    
    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        """Callback when subscription is confirmed"""
        print("Subscribed: " + str(mid) + " " + str(granted_qos))
    
    def on_message(self, client, userdata, msg):
        """Callback when message is received"""
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    
    def connect(self):
        """Connect to MQTT broker"""
        self.client.connect(self.broker, self.port)
    
    def subscribe(self, topic, qos=1):
        """Subscribe to a topic"""
        self.client.subscribe(topic, qos=qos)
    
    def publish(self, topic, payload, qos=1):
        """Publish a message to a topic"""
        self.client.publish(topic, payload=payload, qos=qos)
    
    def start(self):
        """Start the MQTT client loop"""
        self.client.loop_forever()
    
    def __call__(self, topic, payload, qos=1):
        """
        Make the instance callable - publishes a message when called
        
        Args:
            topic: Topic to publish to
            payload: Message payload
            qos: Quality of Service level
        """
        self.publish(topic, payload, qos)


# Usage example
if __name__ == "__main__":
    # Create client instance
    mqtt_client = MQTTClient(
        broker="a27aaea2015146a685292ef3784f2765.s1.eu.hivemq.cloud",
        port=8883,
        username="iotnetwork",
        password="Kenny123@"
    )
    
    # Connect to broker
    mqtt_client.connect()
    
    # Subscribe to topic
    mqtt_client.subscribe("encyclopedia/#", qos=1)
    
    # Publish using regular method
    mqtt_client.publish("encyclopedia/temperature", payload="hot", qos=1)
    
    # Publish using __call__ method (calling the instance directly)
    mqtt_client("encyclopedia/humidity", payload="high", qos=1)
    
    # Start listening
    mqtt_client.start()