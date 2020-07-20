import os
import grpc
import logging
from chief_of_state.service_pb2_grpc import ChiefOfStateServiceStub
from chief_of_state.service_pb2 import ProcessCommandRequest
from sample_app.state_pb2 import State
from google.protobuf.any_pb2 import Any
from google.protobuf.json_format import MessageToJson

logger = logging.getLogger(__name__)

class CosClient():

    @staticmethod
    def process_command(id, command):
        logger.debug("begin process_command")

        command_any = Any()
        command_any.Pack(command)
        logger.debug("make any")
        logger.debug(MessageToJson(command_any))

        cos_request = ProcessCommandRequest(
            entity_uuid = id,
            command = command_any
        )
        logger.debug("wrap in ProcessCommandRequest")
        logger.debug(MessageToJson(cos_request))

        stub = CosClient._get_cos_stub()

        logger.debug("attempt CosClient call")

        try:
            response = stub.ProcessCommand(cos_request)
            logger.debug("CosClient call successful")
            resulting_state = State()
            response.state.Unpack(resulting_state)
            return resulting_state

        except Exception as e:
            logger.error("CosClient call failed", e)
            raise e

    @staticmethod
    def _get_cos_stub():
        host = os.environ.get("COS_HOST")
        port = os.environ.get("COS_PORT")
        logger.debug(f'cos stub host {host}:{port}')

        channel = grpc.insecure_channel(f'{host}:{port}')
        stub = ChiefOfStateServiceStub(channel)

        return stub
