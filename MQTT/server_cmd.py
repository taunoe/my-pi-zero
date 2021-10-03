#!/usr/bin/python3

"""
Devise: Server
Reads data from Broker and sends commands to Broker.
Tauno Erik
03.10.2021
"""

import secrets                  # secrets.py file
import paho.mqtt.client as mqtt # pip3 install paho-mqtt
import time
import json

id = secrets.CLIENT_ID

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + '_nightlight_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    command = { 'led_on' : payload['light'] < 150 }
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)
