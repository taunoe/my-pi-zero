#!/usr/bin/python3

"""
Reads data from Broker and sends commands to Broker.
Tauno Erik
03.10.2021
"""

import settings                 # settings.py file
import paho.mqtt.client as mqtt # pip3 install paho-mqtt
import time
import json

id = settings.CLIENT_ID

topic_telemetry = settings.TOPIC_TELEMETRY
topic_command = settings.TOPIC_COMMAND
client_name = id + 'reader_commander'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect(settings.BROKER)

mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    command = { 'led_on' : payload['light'] < 150 }
    print("Sending message:", command)
    client.publish(topic_command, json.dumps(command))

mqtt_client.subscribe(topic_telemetry)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)
