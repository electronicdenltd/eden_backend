import ssl
import threading
import time
import paho.mqtt.client as mqtt
from decouple import config


class MqttService:
    _client = None
    _connected = False
    _lock = threading.Lock()

    # MQTT Config (EDIT THESE)
    BROKER = config('MQTT_BROKER')
    PORT = config('MQTT_PORT', cast=int)
    USERNAME = config('MQTT_USERNAME')
    PASSWORD = config('MQTT_PASSWORD')

    @classmethod
    def _init_client(cls):
        """Initialize the MQTT client once and start the loop in a thread."""
        with cls._lock:
            if cls._client is not None:
                return  # already initialized

            client = mqtt.Client(
                client_id="django-backend",
                protocol=mqtt.MQTTv311
            )

            client.username_pw_set(cls.USERNAME, cls.PASSWORD)

            # TLS settings
            client.tls_set(
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS
            )

            client.on_connect = cls._on_connect
            client.on_disconnect = cls._on_disconnect
            client.on_publish = cls._on_publish

            cls._client = client

            # Start connection thread
            threading.Thread(
                target=cls._connect_loop,
                daemon=True
            ).start()

    @classmethod
    def _connect_loop(cls):
        """Background thread: try connecting, auto-retry forever."""
        while True:
            if not cls._connected:
                try:
                    print("[MQTT] Connecting to broker…")
                    cls._client.connect(cls.BROKER, cls.PORT)
                except Exception as e:
                    print("[MQTT] Connection failed:", e)
                time.sleep(3)  # retry delay

            # Keep network loop alive
            cls._client.loop(timeout=1.0)
            time.sleep(0.1)

    # --------------------------
    # MQTT CALLBACKS
    # --------------------------
    @staticmethod
    def _on_connect(client, userdata, flags, rc):
        print("[MQTT] Connected with rc =", rc)
        MqttService._connected = True

    @staticmethod
    def _on_disconnect(client, userdata, rc):
        print("[MQTT] Disconnected, rc =", rc)
        MqttService._connected = False

    @staticmethod
    def _on_publish(client, userdata, mid):
        print("[MQTT] Message published! mid =", mid)

    # --------------------------
    # PUBLIC METHOD
    # --------------------------
    @classmethod
    def publish(cls, topic, message, qos=1):
        """
        Public method used anywhere in Django to publish messages.
        Auto-initializes MQTT if needed.
        """
        if cls._client is None:
            cls._init_client()

        if not cls._connected:
            print("[MQTT] WARNING: Not connected. Message queued? → retrying.")
            # Optionally, queue messages or wait
            return False

        try:
            result = cls._client.publish(topic, message, qos=qos)
            return result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception as e:
            print("[MQTT] Publish error:", e)
            return False
        

MqttService.publish("eden/doors/commands","open")