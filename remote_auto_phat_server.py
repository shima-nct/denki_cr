
import socket
import json
import qwiic_scmd
import argparse

# コマンドラインオプションの処理
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=3354)
args = parser.parse_args()

# モータードライバのインスタンス生成
myMotor = qwiic_scmd.QwiicScmd()


def stop_all_motors():
    """
    モータードライバをまとめて止める．
    """
    myMotor.set_drive(0, 0, 0)  # set_drive()の引数はそれぞれ
                                # MOTOR, DIR, SPEED
    myMotor.set_drive(1, 0, 0)


stop_all_motors()  # 念のために止めておく．

timeout_time = 300  # 単位[s]．何も送られて来なければ通信障害を
# 想定してモーターを止める．

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((socket.gethostname(), args.port))
    serversocket.listen()   # サーバーとして接続要求の受付開始．

    while True:
        # 接続要求を受け入れる．
        (clientsocket, address) = serversocket.accept()
        clientsocket.settimeout(timeout_time)  # 受信ソケットにtimeoutを設定
        try:
            while True:
                # 受信データを取り出す．1024はバッファーサイズ．
                json_data = clientsocket.recv(1024)
                clientsocket.sendall(b'R')  # 受領確認として`R`を送る．
                # 受信データはjson形式で表現されている．
                # このデータを連想配列に変換する．
                data = json.loads(json_data.decode("utf-8"))
                # 連想配列のデータ内の各パラメータを取り出してモータードライバに
                # 設定する．
                myMotor.set_drive(data["motor"], data["dir"], data["speed"])
        except:
            stop_all_motors()
            clientsocket.close()
