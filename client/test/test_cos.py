import grpc
from sample_app.api_pb2_grpc import SampleServiceStub
from sample_app.api_pb2 import AppendRequest, GetRequest, CreateRequest
from sample_app.events_pb2 import AppendEvent, CreateEvent
from sample_app.state_pb2 import State
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

        TestCos._test_create(stub)
        TestCos._test_append(stub)

    @staticmethod
    def _test_create(stub):
        print("TestCos.CreateRequest")

        id = "x"
        # create a command
        command = CreateRequest(id = id)

        # wrap in COS request
        cos_request = ProcessCommandRequest(
            entity_uuid = id,
            command = pack_any(command)
        )

        # send to COS
        response = stub.ProcessCommand(cos_request)

        output_state = State()
        response.state.Unpack(output_state)
        assert output_state.id == id

    def _test_append(stub):
        print("TestCos.AppendRequest")

        id = "x"
        # create a command
        command = AppendRequest(id = id, append = 'new')

        # wrap in COS request
        cos_request = ProcessCommandRequest(
            entity_uuid = id,
            command = pack_any(command)
        )

        # send to COS
        response = stub.ProcessCommand(cos_request)

        output_state = State()
        response.state.Unpack(output_state)
        assert output_state.id == id
        assert output_state.values == ['new']


if __name__ == '__main__':
    TestCos.run()
