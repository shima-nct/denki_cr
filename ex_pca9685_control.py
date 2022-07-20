#!/usr/bin/env python3

# Import the RemoteI2CClient class
from remote_i2c import RemoteI2CClient
import time

# Connect to the I2C Host (see docstring for additional args)
# remote_i2c_server.py を動かしている Raspberry PiのIPアドレスを指定
remote_i2c_host = '10.1.101.197'
bus = RemoteI2CClient(remote_i2c_host)
bus.connect()

# Perform I2C operations
# https://github.com/sparkfun/Pi_Servo_Hat/blob/master/Examples/servohat_50Hz.py
addr = 0x40

## Running this program will move the servo to 0, 45, and 90 degrees with 5 second pauses in between with a 50 Hz PWM signal.

bus.write_byte_data(addr, 0, 0x20) # enables word writes
time.sleep(.25)
bus.write_byte_data(addr, 0, 0x10) # enable Prescale change as noted in the datasheet
time.sleep(.25) # delay for reset
bus.write_byte_data(addr, 0xfe, 0x79) #changes the Prescale register value for 50 Hz, using the equation in the datasheet.
bus.write_byte_data(addr, 0, 0x20) # enables word writes

time.sleep(.25)
bus.write_word_data(addr, 0x06, 0) # chl 0 start time = 0us
               
time.sleep(.25)
bus.write_word_data(addr, 0x08, 209) # chl 0 end time = 1.0ms (0 degrees)
time.sleep(5)
bus.write_word_data(addr, 0x08, 312) # chl 0 end time = 1.5ms (45 degrees)
time.sleep(5)
bus.write_word_data(addr, 0x08, 416) # chl 0 end time = 2.0ms (90 degrees)

# Disconnect when you're done, if you feel the need
bus.disconnect()