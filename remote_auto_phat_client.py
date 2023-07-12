import socket
import json
import time
import argparse

# コマンドラインオプションの処理
parser = argparse.ArgumentParser()
parser.add_argument("--remote-host", type=str, default=socket.gethostname())
parser.add_argument("--remote-port", type=int, default=3354)
args = parser.parse_args()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((args.remote_host, args.remote_port))

    def send_control(control):
        json_data = json.dumps(control).encode('utf-8')
        s.sendall(json_data)
        return_code = ''
        while True:
            return_code = s.recv(1024)
            if return_code == b'R':
                break
        return return_code

    try:
        while True:
            for speed in range(20, 255):
                control = {"motor": 0, "dir": 0, "speed": speed}
                return_code = send_control(control)
                time.sleep(0.01)
            for speed in range(254, 20, -1):
                control = {"motor": 0, "dir": 0, "speed": speed}
                return_code = send_control(control)
                time.sleep(0.01)
    finally:
        control = {"motor": 0, "dir": 0, "speed": 0}
        return_code = send_control(control)
        control = {"motor": 1, "dir": 0, "speed": 0}
        return_code = send_control(control)

