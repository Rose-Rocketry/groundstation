###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose

import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes 
import time,logging,sys

client_id="testclient2"
mqttv=mqtt.MQTTv5
messages=[]
host = '192.168.1.41'
port=1883
pub_topic="house/sensor1"

def on_connect(client, userdata, flags, reasonCode,properties=None):
    print('Connected ',flags)
    #print('Connected properties',properties)
    #print('Connected ',reasonCode)



def on_message(client, userdata, message):

    msg=str(message.payload.decode("utf-8"))
    messages.append(msg)
    print('RECV Topic = ',message.topic)
    print('RECV MSG =', msg)


def on_disconnect(client, userdata, rc,properties=None):
    print('Received Disconnect ',rc)

def on_subscribe(client, userdata, mid, granted_qos,properties=None):
    print('SUBSCRIBED')

def on_unsubscribe(client, userdata, mid, properties, reasonCodes):
    print('UNSUBSCRIBED') 



print("creating client with clean session=False and then subscribing")
print("session will expire in 30 seconds")
client_sub = mqtt.Client("subclient",protocol=mqttv)
client_pub = mqtt.Client("pubclient",protocol=mqttv)

client_sub.on_connect = on_connect
client_pub.on_connect = on_connect
client_sub.on_message = on_message
client_sub.on_disconnect = on_disconnect
client_sub.on_subscribe = on_subscribe

properties=Properties(PacketTypes.CONNECT)
print("Setting session expiry interval")
properties.SessionExpiryInterval=30 #set session expiry interval
#properties=None
client_sub.connect(host,clean_start=False,properties=properties)
#client_sub.connect(host,clean_start=True,properties=properties)
client_sub.loop_start()
client_sub.subscribe('test',qos=1)

time.sleep(5)
print("sub_client Disconnecting")
client_sub.disconnect()
client_sub.loop_stop()
print("Pub_client Connecting and will publish while receiver disconnected")

client_pub.connect(host)
msg_out1="Testing session expire interval- part1"
print("Publishing messages while disconnected")
client_pub.publish('test', msg_out1,qos=1)
print(" waiting 20 seconds= ")
time.sleep(20)
print(" connecting expect to receive message")

client_sub.connect(host,clean_start=False,properties=properties)
#client_sub.connect(host,clean_start=True,properties=properties)
client_sub.loop_start()
#client_sub.subscribe('test', qos=1)
time.sleep(5) #wait to receive message
if len(messages)==0:
    print("test failed")
else:
    msg=messages.pop()
    if msg==msg_out1:
        print("test succeeded")
###Part 2

properties=Properties(PacketTypes.CONNECT)
print("Setting session expiry interval")
properties.SessionExpiryInterval=30 #set session expiry interval
#properties=None
client_sub.connect(host,clean_start=False,properties=properties)
#client_sub.connect(host,clean_start=True,properties=properties)
client_sub.loop_start()
client_sub.subscribe('test',qos=1)

time.sleep(5)
print("sub_client Disconnecting")
client_sub.disconnect()
client_sub.loop_stop()
print("Pub_client Connecting and will publish while receiver disconnected")

client_pub.connect(host)
msg_out1="Testing session expire interval- part2"
print("Publishing messages while disconnected")
client_pub.publish('test', msg_out1,qos=1)
print(" waiting 40 seconds= ")
time.sleep(40)
print(" connecting dont't expect to receive messages as session should have expired")

client_sub.connect(host,clean_start=False,properties=properties)

client_sub.loop_start()

time.sleep(5) #wait to receive message
if len(messages)==0:
    print("test succeeded")
else:
    msg=messages.pop()
    if msg==msg_out1:
        print("test failed")
client_sub.loop_stop()
client_sub.disconnect()
client_pub.disconnect()
