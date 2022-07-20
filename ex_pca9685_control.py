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
# PCA9685 16-channel, 12-bit PWM Fm+ I2C-bus LED controller
# https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf
addr = 0x40

## Running this program will move the servo to 0, 45, and 90 degrees with 5 second pauses in between with a 50 Hz PWM signal.

# MODE1 register 
# https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf#page=10
# 7.3.1 Mode register 1, MODE1
# https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf#page=14
# enables word writes. 
#   Register Auto-Increment enabled.
MODE1 = 0   
bus.write_byte_data(addr, MODE1, 0x20) 
time.sleep(.25)
# enable Prescale change as noted in the datasheet
#   Low power mode. Oscillator off[3][4].
#   [3] No PWM control is possible when the oscillator is off.
#   [4] When the oscillator is off (Sleep mode) the LEDn outputs cannot be turned on, off or dimmed/blinked
bus.write_byte_data(addr, MODE1, 0x10) 
time.sleep(.25) # delay for reset

# PRE_SCALE register
# https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf#page=13
# 7.3.5 PWM frequency PRE_SCALE
# https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf#page=25
# changes the Prescale register value for 50 Hz, using the equation in the datasheet.
#   prescaler for PWM output frequency
#   [1] Writes to PRE_SCALE register are blocked when SLEEP bit is logic 0 (MODE 1)
PRE_SCALE = 0xfe
bus.write_byte_data(addr, PRE_SCALE, 0x79) 
bus.write_byte_data(addr, MODE1, 0x20) # enables word writes
time.sleep(.25)

# LED0_ON_L register
# https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf#page=10
# 7.3.3 LED output and PWM control
# https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf#page=16
LED0_ON_L=0x06
bus.write_word_data(addr, LED0_ON_L, 0) # chl 0 start time = 0us   
time.sleep(.25)

# LED0_OFF_L register
# https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf#page=10
# 7.3.3 LED output and PWM control
# https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf#page=16
bus.write_word_data(addr, 0x08, 209) # chl 0 end time = 1.0ms (0 degrees)
time.sleep(5)
bus.write_word_data(addr, 0x08, 312) # chl 0 end time = 1.5ms (45 degrees)
time.sleep(5)
bus.write_word_data(addr, 0x08, 416) # chl 0 end time = 2.0ms (90 degrees)

# Disconnect when you're done, if you feel the need
bus.disconnect()