import paho.mqtt.client as mqtt
import platform


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client: mqtt.Client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))

    client.subscribe("rocket/+/+/#", qos=2)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"{msg.topic} ({len(msg.payload)} bytes) {msg.payload}")


client = mqtt.Client(platform.node(), protocol=mqtt.MQTTv5)
print(f"client_id={platform.node()}")
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker", clean_start=False)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
