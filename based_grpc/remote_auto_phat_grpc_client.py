import argparse
import time
import grpc
import auto_phat_pb2
import auto_phat_pb2_grpc

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote-host", type=str, default='0.0.0.0')
    parser.add_argument("--remote-port", type=int, default=3354)
    args = parser.parse_args()

    host = '{}:{}'.format(args.remote_host,args.remote_port)
    with grpc.insecure_channel(host) as channel:
        stub = auto_phat_pb2_grpc.ControlStub(channel)

        def motor_drive(speed):
            for motor in range(0,2):
                req = auto_phat_pb2.Motor(motor=motor,dir=0,speed=speed)
                response = stub.setMorter(req)

        while True:
            for speed in range(20,256):
                motor_drive(speed)
                time.sleep(0.01)
            for speed in range(254,19,-1):
                motor_drive(speed)
                time.sleep(0.01)


if __name__ == '__main__':
    main()
    