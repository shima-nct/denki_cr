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