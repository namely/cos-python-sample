import grpc
from sample_app.api_pb2_grpc import SampleServiceStub
from sample_app.api_pb2 import AppendRequest, GetRequest, CreateRequest
from sample_app.state_pb2 import State
from google.protobuf.json_format import MessageToJson
from test.helpers import get_channel

class TestApi():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port)
        stub = SampleServiceStub(channel)

        TestApi.create(stub)
        TestApi.append(stub)
        TestApi.get(stub)

    @staticmethod
    def create(stub):
        print("TestApi.create")
        id = "x"
        request = CreateRequest(id = id)
        response = stub.CreateCall(request)
        print(MessageToJson(response))

        assert isinstance(response, State)
        assert response.id == id


    @staticmethod
    def append(stub):
        print("TestApi.append")
        id = "x"
        value = "y"
        request = AppendRequest(id = id, append = value)
        response = stub.AppendCall(request)
        print(MessageToJson(response))
        assert isinstance(response, State)
        assert response.id == id

    @staticmethod
    def get(stub):
        print("TestApi.get")
        id = "x"
        value = "y"
        request = GetRequest(id = id)
        response = stub.GetCall(request)
        print(MessageToJson(response))
        print("done.")



if __name__ == '__main__':
    TestApi.run()
