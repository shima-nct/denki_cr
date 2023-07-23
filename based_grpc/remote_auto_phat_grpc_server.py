import threading
import time
import qwiic_scmd
import argparse

from concurrent.futures import ThreadPoolExecutor
import grpc
import auto_phat_pb2 as auto_phat_pb2
import auto_phat_pb2_grpc as auto_phat_pb2_grpc

# モータードライバのインスタンス生成
myMotor = qwiic_scmd.QwiicScmd()
if myMotor.connected == False:
    raise Exception("Motor Driver not connected. Check connections.")


def stop_all_motors():
    """
    モータードライバをまとめて止める．
    """
    myMotor.set_drive(0, 0, 0)  # set_drive()の引数はそれぞれ
    # MOTOR, DIR, SPEED
    myMotor.set_drive(1, 0, 0)


myMotor.begin()
print("Motor initialized.")
time.sleep(.250)
stop_all_motors()  # 念のために止めておく．
myMotor.enable()
print("Motor enabled")
time.sleep(.250)


class Control(auto_phat_pb2_grpc.ControlServicer):

    watchdog_timer_duration = 1.0

    def __init__(self):
        # ウォッチドックタイマー用に現在の時刻を記録
        self.last_called = time.time()
        # ウォッチドックタイマーのセットアップ
        self.watchdog_timer = threading.Timer(
            self.watchdog_timer_duration, self.watchdog_check)
        self.watchdog_timer.start()

    def setMorter(self, request, context):
        self.last_called = time.time()  # 呼び出された時刻に更新
        myMotor.set_drive(request.motor, request.dir, request.speed)
        return auto_phat_pb2.Response(error=False)

    def watchdog_check(self):
        # setMoter()を呼び出してから5秒を越えていたらモーターを停止
        if time.time() - self.last_called > self.watchdog_timer_duration:
            stop_all_motors()

        # ウォッチドックタイマーをリセット
        self.watchdog_timer = threading.Timer(
            self.watchdog_timer_duration, self.watchdog_check)
        self.watchdog_timer.start()


def main():
    # コマンドラインオプションの処理
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=3354)
    args = parser.parse_args()

    server = grpc.server(ThreadPoolExecutor(max_workers=2))
    control = Control()
    auto_phat_pb2_grpc.add_ControlServicer_to_server(control, server)
    server.add_insecure_port('[::]:{}'.format(args.port))
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:   # Ctrl+Cを押されたら終了
        control.watchdog_timer.cancel()
        stop_all_motors()
        server.stop(None)   # 猶予期間が指定されていない場合 (None を渡す)，
        # 既存のすべての RPC は直ちに中止され、最後の
        # RPC ハンドラが終了するまでこのメソッドはブロ
        # ックされます．
        # https://grpc.github.io/grpc/python/grpc.html
        print("Interrupted by user, shutting down.")

if __name__ == '__main__':
    main()
