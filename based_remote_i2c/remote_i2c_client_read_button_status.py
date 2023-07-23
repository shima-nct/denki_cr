#!/usr/bin/env python3

import argparse
import time
# Import the RemoteI2CClient class
from remote_i2c import RemoteI2CClient

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

# Perform I2C operations
# Qwiic Quad Relayのアドレス 0x6d
# Qwiic Buttonのアドレス 0x6f
addr = 0x6f

# https://learn.sparkfun.com/tutorials/sparkfun-qwiic-button-hookup-guide/all#register-map
button_status_reg = 0x03
led_brightness_reg = 0x19

led_brightness = 0
max_led_brightness = 100

def clear_status():
    """
    Qwiic Buttionのステータスレジスタをクリアします．
    """
    bus.write_byte_data(addr, button_status_reg, 0)


def get_button_status():
    """
    Qwiic Buttionのステータスレジスタの値を取得して，
    その値とボタンがクリックされたか等の値を返します．
    """
    value = bus.read_byte_data(addr, button_status_reg)
    # 0桁目 イベントが起こったなら1，なければ0
    # 1桁目 クリックされたなら1, なければ0
    # 2桁目 ステータスを取得した際に押されていたなら1，無ければ0
    event_available = bool(value & 1 << 0)
    has_been_clicked = bool(value & 1 << 1)
    is_pressed = bool(value & 1 << 2)
    return (value, event_available, has_been_clicked, is_pressed)

def get_led_brightness():
    """
    Qwiic ButtionのLED（LEDが付いているならば）の明るさ（0-255）の値を取得します．
    """
    return bus.read_byte_data(addr, led_brightness_reg)

def set_led_brightness(value):
    """
    Qwiic ButtionのLED（LEDが付いているならば）の明るさ（0-255）を設定します．
    """
    bus.write_byte_data(addr, led_brightness_reg, value)


clear_status()
set_led_brightness(0)
while True:
    try:
        (value,
         event_available,
         has_been_clicked,
         is_pressed) = get_button_status()
        # 0桁目 イベントが起こったなら1，なければ0
        # 1桁目 クリックされたなら1, なければ0
        # 2桁目 ステータスを取得した際に押されていたなら1，無ければ0
        current_led_brightness = get_led_brightness()
        print("Status: {:#05b}, LED: {}".format(value, current_led_brightness))

        if event_available:
            if is_pressed:
                led_brightness = max_led_brightness if led_brightness == 0 else 0
                set_led_brightness(led_brightness)

            clear_status()
        time.sleep(1)

    except KeyboardInterrupt as e:
        break
    
clear_status()
print("Close connection")
# Disconnect when you're done, if you feel the need
bus.disconnect()

