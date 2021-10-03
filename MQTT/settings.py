#!/usr/bin/python3
"""
  settings.py
  Tauno Erik
  03.10.2021
"""

BROKER = 'test.mosquitto.org'  #
ID = 'MYuniqueID'              # Generator https://www.guidgen.com/
TOPIC_TELEMETRY = ID + '/telemetry'
TOPIC_COMMAND = ID + '/commands'
