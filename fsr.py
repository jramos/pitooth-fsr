#!/usr/bin/python2.7

import os
import sys
import time
import RPi.GPIO as GPIO

LED_PIN = 5
FSR_PIN = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(FSR_PIN, GPIO.IN)
GPIO.output(LED_PIN, False)

previous_value = 1

try:
  while True:
    value     = GPIO.input(FSR_PIN)
    led_value = GPIO.input(LED_PIN)

    if (value == 0):
      if (previous_value != 0):
        GPIO.output(LED_PIN, not led_value)
        os.system("/usr/local/bin/keystroke")
        time.sleep(1)

    previous_value = value
    time.sleep(0.1)

finally:
  GPIO.cleanup()