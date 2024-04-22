import grpc
import echo_pb2
import echo_pb2_grpc

def run():
    channel = grpc.insecure_channel('10.8.6.34:50051')
    stub = echo_pb2_grpc.EchoServiceStub(channel)
    response = stub.Echo(echo_pb2.EchoRequest(message='hello'))
    print("Echo received: " + response.message)

if __name__ == '__main__':
    run()
