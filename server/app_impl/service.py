from concurrent import futures
import logging
import grpc
import app.api_pb2_grpc
from app.api_pb2 import (AppendRequest, GetRequest, State)
from app_impl.validation import StatelessValidation


class TestServiceImpl(app.api_pb2_grpc.TestServiceServicer):
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
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    app.api_pb2_grpc.add_TestServiceServicer_to_server(TestServiceImpl(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()
    logging.info("killing server")
