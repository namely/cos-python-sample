import grpc
from sample_app.api_pb2_grpc import SampleServiceStub
from sample_app.api_pb2 import AppendRequest, GetRequest
from google.protobuf.json_format import MessageToJson
from test.helpers import get_channel

class TestApi():
    @staticmethod
    def run():
        host = "api"
        port = "9090"

        channel = get_channel(host, port)

        id = "x"
        value = "y"

        TestApi.append(channel, id, value)
        TestApi.get(channel, id)

    @staticmethod
    def append(channel, id, value):
        print("APPEND")
        stub = SampleServiceStub(channel)
        request = AppendRequest(id = id, append = value)
        response = stub.AppendCall(request)
        print(MessageToJson(response))
        print("done.")

    @staticmethod
    def get(channel, id):
        print("GET")
        stub = SampleServiceStub(channel)
        request = GetRequest(id = id)
        response = stub.GetCall(request)
        print(MessageToJson(response))
        print("done.")



if __name__ == '__main__':
    TestApi.run()
