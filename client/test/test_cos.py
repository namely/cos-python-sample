import grpc
from sample_app.api_pb2_grpc import SampleServiceStub
from sample_app.api_pb2 import AppendRequest, GetRequest, CreateRequest
from chief_of_state.service_pb2_grpc import ChiefOfStateServiceStub
from chief_of_state.service_pb2 import ProcessCommandRequest
from google.protobuf.json_format import MessageToJson
from test.helpers import get_channel, pack_any, unpack_any
from google.protobuf.any_pb2 import Any


class TestCos():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port)
        stub = ChiefOfStateServiceStub(channel)

        print("TestCos.ProcessCommand")

        id = "x"

        # create a command
        command = CreateRequest(id = id)

        # wrap in COS request
        cos_request = ProcessCommandRequest(
            entity_uuid = id,
            command = pack_any(command)
        )

        print(MessageToJson(cos_request))

        # send to COS
        response = stub.ProcessCommand(cos_request)

        print(MessageToJson(response))


if __name__ == '__main__':
    TestCos.run()
