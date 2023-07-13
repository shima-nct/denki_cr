import socket
import json
import time
import sys
import argparse


# コマンドラインオプションの処理
parser = argparse.ArgumentParser()
parser.add_argument("--remote-host", type=str, default='0.0.0.0')
parser.add_argument("--remote-port", type=int, default=3354)
args = parser.parse_args()

buffer_size = 1024


def send_control(stream, control):
    json_data = json.dumps(control).encode('utf-8')
    stream.sendall(json_data)
    return_code = ''
    while True:
        return_code = stream.recv(buffer_size)
        if return_code == b'R':
            break
    return return_code


def send_two_motor(_stream, _speed):
    for motor in range(0, 2):
        control = {"motor": motor, "dir": 0, "speed": _speed}
        send_control(_stream, control)
        control = {"motor": motor, "dir": 0, "speed": _speed}
        send_control(_stream, control)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
        stream.connect((args.remote_host, args.remote_port))

        try:
            while True:
                for speed in range(20, 255):
                    send_two_motor(stream, speed)
                    time.sleep(0.01)
                for speed in range(254, 20, -1):
                    send_two_motor(stream, speed)
                    time.sleep(0.01)
        except:
            send_two_motor(stream, 0)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as e:
        sys.exit(0)
