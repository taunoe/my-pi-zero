#!/usr/bin/python3

"""
Devise: Sensor
Sends data to Broker.
Tauno Erik
02.10.2021
"""

import secrets                  # secrets.py file
import paho.mqtt.client as mqtt # pip3 install paho-mqtt
import time
import json

ENVIRONMENT = 'dev'

id = secrets.CLIENT_ID

client_telemetry_topic = id + '/telemetry'
client_name = id + 'nightlight_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")

####
def read_sensor_real():
  #TODO
  return 0

def create_sensor():
  value = 0

  def read_value():
    return value
  
  def increment():
    nonlocal value
    value += 1
    if value > 1024:
      value = 0
  
  return (read_value, increment)

read_virtual_value, increment_virtual_value = create_sensor()

def read_sensor_virtual():
  increment_virtual_value()
  value = read_virtual_value()
  return value

read_sensor = read_sensor_real if ENVIRONMENT == 'prod' else read_sensor_virtual

####

while True:
    light = read_sensor()
    telemetry = json.dumps({'light' : light})

    print("Sending telemetry ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)