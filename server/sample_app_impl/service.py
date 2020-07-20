from concurrent import futures
import logging
import grpc
import os
from sample_app.api_pb2 import (AppendRequest, GetRequest)
from sample_app.state_pb2 import State
from sample_app.api_pb2_grpc import SampleServiceServicer
from sample_app.api_pb2_grpc import add_SampleServiceServicer_to_server
from chief_of_state.service_pb2_grpc import ChiefOfStateServiceStub
from .validation import StatelessValidation
from .cos_client import CosClient


class SampleServiceImpl(SampleServiceServicer):
    def AppendCall(self, request, context):

        # do stateless validation
        StatelessValidation.validate(request)

        # send to chief of state, get resulting state
        state = CosClient.process_command(request.id, request)

        # convert back to gRPC expected response
        return state

    def GetCall(self, request, context):
        # send to chief of state, get resulting state
        state = State(
            id=request.id,
            values=["a"]
        )

        # convert back to gRPC expected response
        return state


def run(port):
    logging.basicConfig()
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
