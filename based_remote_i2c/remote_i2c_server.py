#!/usr/bin/env python3

# Import the RemoteI2CServer class
from remote_i2c import RemoteI2CServer

# Create the server (see docstring for additional args)
# デフォルトでは5446ポートで待ち受け．
server = RemoteI2CServer()

# Start the server (blocks forever!)
server.serve()
