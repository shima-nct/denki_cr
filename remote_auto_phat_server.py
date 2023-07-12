
import socket
import json
import qwiic_scmd
import argparse

# コマンドラインオプションの処理
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=3354)
args = parser.parse_args()

myMotor = qwiic_scmd.QwiicScmd()

def stop_all_motors():
    # (MOTOR, DIR, SPEED)
    myMotor.set_drive(0, 0, 0)
    myMotor.set_drive(1, 0, 0)

stop_all_motors()

timeout_time = 300  # [s]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((socket.gethostname(), args.port))
    serversocket.listen()

    try:
        while True:
            (clientsocket, address) = serversocket.accept()
            clientsocket.settimeout(timeout_time)
            try:
                while True:
                    json_data = clientsocket.recv(1024)
                    if not json_data:
                        break
                    clientsocket.sendall(b'R')
                    data = json.loads(json_data.decode("utf-8"))
                    myMotor.set_drive(data["motor"], data["dir"], data["speed"])
            except socket.timeout:
                stop_all_motors()
                clientsocket.close()
    finally:
        stop_all_motors()