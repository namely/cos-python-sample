from concurrent import futures
import logging
import grpc
from sample_app.api_pb2 import (AppendRequest, GetRequest)
from sample_app.state_pb2 import State
from sample_app.api_pb2_grpc import SampleServiceServicer
from sample_app.api_pb2_grpc import add_SampleServiceServicer_to_server
from .validation import StatelessValidation


class SampleServiceImpl(SampleServiceServicer):
    def AppendCall(self, request, context):

        # do stateless validation
        StatelessValidation.validate(request)

        # send to chief of state, get resulting state
        state = State(
            id=request.id,
            values=[request.append]
        )

        # convert back to gRPC expected response
        return state

    def GetCall(self, request, context):
        # send to chief of state, get resulting state
        state = State(
            id=request.id,
            values=[]
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
