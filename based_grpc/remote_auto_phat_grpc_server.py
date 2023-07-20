
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
    def setMorter(self, request, context):
        myMotor.set_drive(request.motor, request.dir, request.speed)
        return auto_phat_pb2.Response(error=False)


def main():
    # コマンドラインオプションの処理
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=3354)
    args = parser.parse_args()

    server = grpc.server(ThreadPoolExecutor(max_workers=2))
    auto_phat_pb2_grpc.add_ControlServicer_to_server(Control(), server)
    server.add_insecure_port('[::]:{}'.format(args.port))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
