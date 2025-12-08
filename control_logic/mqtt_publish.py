import paho.mqtt.client as mqtt
import ssl
import time

BROKER = "42a20965c540410ba497e160a8857827.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "famous"
PASSWORD = "mqtt2025Famous@iot"
TOPIC = "eden/door/status"

def on_connect(client, userdata, flags, rc):
    print("Connected:", rc)
    # Publish immediately after connection
    client.publish(TOPIC, "hello from python!", qos=1)

def on_publish(client, userdata, mid):
    print("Message published! mid =", mid)


client = mqtt.Client(
    client_id="python-publisher",
    protocol=mqtt.MQTTv311     # FORCE MQTT v3.1.1
)

client.username_pw_set(USERNAME, PASSWORD)

client.tls_set(
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS
)

client.on_connect = on_connect
client.on_publish = on_publish

print("Connecting to HiveMQ Cloud…")
client.connect(BROKER, PORT)

client.loop_start()

# give time for publish & ACK
time.sleep(3)

client.loop_stop()
client.disconnect()
print("Done.")
