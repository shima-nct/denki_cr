#!/usr/bin/env python3

# Import the RemoteI2CClient class
import argparse
from remote_i2c import RemoteI2CClient
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

# Perform I2C operations
# Qwiic Quad Relayのアドレス 0x6d 
# Qwiic Buttonのアドレス　
addr = 0x6d
on_value = 0x0b     # All on
off_value = 0x0a    # All off

# アドレス 0x6d に1を書き込むと1番リレーの ON/OFF 状態が入れ替わります入れ替わり(toggle)ます．
# 2を書き込むと1番リレーの ON/OFF 状態が入れ替わります入れ替わります．
# 3，４を書きこんだ場合も同様です．
# toggle1_value =  0x01
# toggle2_value =  0x02
# toggle3_value =  0x03
# toggle4_value =  0x04

#ret = bus.read_byte_data(addr)

bus.write_byte(addr, on_value)
time.sleep(1)

bus.write_byte(addr, off_value)
time.sleep(1)

# Disconnect when you're done, if you feel the need
bus.disconnect()