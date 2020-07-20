from concurrent import futures
import logging
import grpc
import os
import sys
from sample_app.api_pb2 import (CreateRequest, AppendRequest, GetRequest)
from sample_app.state_pb2 import State
from sample_app.api_pb2_grpc import SampleServiceServicer
from sample_app.api_pb2_grpc import add_SampleServiceServicer_to_server
from chief_of_state.service_pb2_grpc import ChiefOfStateServiceStub
from .validation import StatelessValidation
from .cos_client import CosClient
from google.protobuf.json_format import MessageToJson


logger = logging.getLogger(__name__)

class SampleServiceImpl(SampleServiceServicer):

    def CreateCall(self, request, context):
        logger.debug("begin CreateCall")
        logger.debug(MessageToJson(request))
        # do stateless validation
        StatelessValidation.validate(request)
        # send to chief of state, get resulting state
        return CosClient.process_command(request.id, request)

    def AppendCall(self, request, context):
        # do stateless validation
        StatelessValidation.validate(request)
        # send to chief of state, get resulting state
        return CosClient.process_command(request.id, request)

    def GetCall(self, request, context):
        # send to chief of state, get resulting state
        return CosClient.process_command(request.id, request)


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def run(port):
    configure_logging()
    logging.info("starting server")

    # define grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # add grpc implementation to server
    add_SampleServiceServicer_to_server(SampleServiceImpl(), server)
    # set port
    server.add_insecure_port(f'[::]:{port}')
    # start
    server.start()
    server.wait_for_termination()
    logging.info("killing server")
