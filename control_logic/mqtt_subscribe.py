import paho.mqtt.client as mqtt
import ssl

# -------------------------
# HiveMQ Configuration
# -------------------------
BROKER = "YOUR_HIVEMQ_HOST"     # e.g. "yourcluster.hivemq.cloud"
PORT = 8883                     # TLS port
USERNAME = "your_username"
PASSWORD = "your_password"
TOPIC = "test/topic"

# -------------------------
# Callbacks
# -------------------------
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to HiveMQ successfully!")
        client.subscribe(TOPIC)
    else:
        print("Connection failed:", reason_code)

def on_message(client, userdata, msg):
    print(f"[MESSAGE] {msg.topic}: {msg.payload.decode()}")

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code", rc)

# -------------------------
# Client Setup
# -------------------------
client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,    # needed for paho v2.x
    client_id="python-test-client"
)

client.username_pw_set(USERNAME, PASSWORD)

# TLS Setup (needed for HiveMQ Cloud)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)

# Attach callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# -------------------------
# Connect
# -------------------------
print("Connecting to HiveMQ...")
client.connect(BROKER, PORT)

# -------------------------
# Keep script running forever
# -------------------------
client.loop_forever()
