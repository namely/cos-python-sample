import os
import grpc
from chief_of_state.service_pb2_grpc import ChiefOfStateServiceStub
from chief_of_state.service_pb2 import ProcessCommandRequest
from google.protobuf.any_pb2 import Any


class CosClient():
    @staticmethod
    def _get_cos_stub():
        host = os.environ.get("COS_HOST")
        port = os.environ.get("COS_PORT")
        channel = grpc.insecure_channel(f'{host}:{port}')
        return ChiefOfStateServiceStub(channel)

    @staticmethod
    def process_command(id, command):
        cos_request = ProcessCommandRequest(
            entity_uuid = id,
            command = Any().Pack(command)
        )

        stub = CosClient._get_cos_stub()

        return stub.ProcessCommand(cos_request)
