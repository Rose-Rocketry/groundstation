import paho.mqtt.client as mqtt
import platform, time


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client: mqtt.Client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))

    client.subscribe("/rocket/+/+/#", qos=2)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client(platform.node(), protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker", clean_start=False)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

lat = 394836300
lon = -873274990
alt = 500000
vel = (100, 100, 500000)

while True:
    time.sleep(1)

    client.publish("rocket/test/1/pos_wgs84",
                   f"{time.time()},{lat * 1e-7},{lon * 1e-7},{alt * 1e-3}")
    client.publish("rocket/test/1/vel_ned",
                   f"{time.time()},{vel[0]},{vel[1]},{vel[2]}")
