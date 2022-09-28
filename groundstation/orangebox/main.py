import paho.mqtt.client as mqtt
import platform, threading
from file_opener import FileOpener
from pathlib import Path

DATA_PATH = Path("/data")
ROCKET_TOPIC = "rocket/+/+/#"
LOG_TOPICS = ["$SYS/broker/uptime", "$SYS/broker/messages/received"]


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client: mqtt.Client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))

    client.subscribe(ROCKET_TOPIC, qos=2)
    for topic in LOG_TOPICS:
        client.subscribe(topic, qos=0)


# The callback for when a PUBLISH message is received from the server.
def on_rocket_message(client: mqtt.Client(), userdata, msg: mqtt.MQTTMessage):
    print(f"{msg.topic} ({len(msg.payload)} bytes) {msg.payload}")
    try:
        text = msg.topic + ":" + msg.payload.decode()
        if "\n" in text:
            raise ValueError(
                f"WARNING: newline contained in message, not logging to file: {msg.payload}"
            )

        tail, launch = msg.topic.split("/")[1:3]

        path = DATA_PATH / tail / (launch + ".txt")

        # Throws an error if directory traversal is detected
        path.resolve().relative_to(DATA_PATH)

        FileOpener.append_line_to_file(path, text)
    except Exception as e:
        print("Error logging message:", e)

# The callback for when a PUBLISH message is received from the server.
def log_packet_only(client: mqtt.Client(), userdata, msg: mqtt.MQTTMessage):
    print(f"{msg.topic} ({len(msg.payload)} bytes) {msg.payload}")


client = mqtt.Client(platform.node(), protocol=mqtt.MQTTv5)
print(f"client_id={platform.node()}")
client.on_connect = on_connect
client.message_callback_add(ROCKET_TOPIC, on_rocket_message)

# for topic in LOG_TOPICS:
#     client.message_callback_add(topic, log_packet_only)

client.connect("broker", clean_start=False)

threading.Thread(target=FileOpener.cleanup_thread,
                 daemon=True,
                 name="Open File Cleanup Thread").start()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
