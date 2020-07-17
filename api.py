from concurrent import futures
import logging

import grpc

import app.api_pb2_grpc
from app.api_pb2 import (Request, Response, State)

class TestServiceImpl(app.api_pb2_grpc.TestServiceServicer):
    def UnaryCall(self, request, context):

        return Response(
            state=State(
                id=request.id,
                values=[request.append_me]
            )
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    app.api_pb2_grpc.add_TestServiceServicer_to_server(TestServiceImpl(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
