#!/usr/bin/env python3

# Import the RemoteI2CClient class
import argparse
from remote_i2c import RemoteI2CClient
import sys
import time

# コマンドラインオプションの処理
parser = argparse.ArgumentParser()
parser.add_argument("--remote-host", type=str, default="0.0.0.0")
parser.add_argument("--remote-port", type=int, default=5446)
args = parser.parse_args()

# Connect to the I2C Host (see docstring for additional args)
# remote_i2c_server.py を動かしている Raspberry PiのIPアドレスを指定
# コマンドラインオプションでリモートホストアドレスを指定しない場合は remote_i2c_host に直接代入するように書き換えてください．
remote_i2c_host = args.remote_host
remote_port = args.remote_port
bus = RemoteI2CClient(remote_i2c_host, remote_port)
bus.connect()

# device address
_QWIIC_BUTTON_DEFAULT_ADDRESS = 0x6F
addr = _QWIIC_BUTTON_DEFAULT_ADDRESS

# Device ID for all Qwiic Buttons
DEV_ID = 0x5D

# Registers
ID = 0x00
FIRMWARE_MINOR = 0x01
FIRMWARE_MAJOR = 0x02
BUTTON_STATUS = 0x03
INTERRUPT_CONFIG = 0x04
BUTTON_DEBOUNCE_TIME = 0x05
PRESSED_QUEUE_STATUS = 0x07
PRESSED_QUEUE_FRONT = 0x08
PRESSED_QUEUE_BACK = 0x0C
CLICKED_QUEUE_STATUS = 0x10
CLICKED_QUEUE_FRONT = 0x11
CLICKED_QUEUE_BACK = 0x15
LED_BRIGHTNESS = 0x19
LED_PULSE_GRANULARITY = 0x1A
LED_PULSE_CYCLE_TIME = 0x1B
LED_PULSE_OFF_TIME = 0x1D
I2C_ADDRESS = 0x1F

#
id = bus.read_byte_data(addr, ID)
if(id != DEV_ID):
    print("Qwiic button is missing.")
    exit()

# Sets all button status bits (is_pressed, has_been_clicked,
# and event_available) to zero.
# First, read BUTTON_STATUS register
button_status = bus.read_byte_data(addr, BUTTON_STATUS)
# Convert to binary and clear the last three bits
button_status = int(button_status) & ~(0x7)
# Write to BUTTON_STATUS register
bus.write_byte(addr, BUTTON_STATUS, button_status)

try:
    last_is_pressed = 0
    while(True):
        # Read the button status register
        button_status = bus.read_byte_data(addr, BUTTON_STATUS)
        # Convert to binary and clear all bits but is_pressed
        is_pressed = int(button_status) & ~(0xFB)
        # Shift is_pressed to the zero bit
        is_pressed = is_pressed >> 2

        # print("button status: %x" % button_status)

        if(is_pressed!=last_is_pressed):
            if(is_pressed):
                print("Button is pressed. Status: %x" % button_status)
            elif(last_is_pressed):
                print("Button is released. Status: %x" % button_status)

        last_is_pressed = is_pressed
except:    
    # Disconnect when you're done, if you feel the need
    bus.disconnect()
