#!/usr/bin/python3

"""
Devise: LED
Reads command from Broker.
Tauno Erik
03.10.2021
"""

import secrets                  # secrets.py file
import paho.mqtt.client as mqtt # pip3 install paho-mqtt
import time
import json

ENVIRONMENT = 'dev'


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
      value = 1024

  def decrement():
    nonlocal value
    value -= 1
    if value < 0:
      value = 0
  
  return (read_value, increment, decrement)

def create_led():
  status = False

  def read_status():
    return status

  def led_on():
    nonlocal status
    status = True
    increment_value()
  
  def led_off():
    nonlocal status
    status = False
    decrement_value()

  return (read_status, led_on, led_off)
  

def read_sensor_virtual():
  #increment_value()
  value = read_value()
  return value


def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['led_on']:
        led_on()
    else:
        led_off()


# Create virtual sensor
read_value, increment_value, decrement_value = create_sensor()
read_sensor = read_sensor_real if ENVIRONMENT == 'prod' else read_sensor_virtual

# Create virtual LED
led_status, led_on, led_off = create_led()


# MQTT
id = secrets.CLIENT_ID
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'nightlight_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

mqtt_client.loop_start()

print("MQTT connected!")

while True:
    light = read_sensor()
    print('Light level:', light)

    telemetry = json.dumps({'light' : light})
    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)