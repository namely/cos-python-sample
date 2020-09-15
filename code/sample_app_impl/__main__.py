from sample_app_impl.service import SampleServiceImpl
from shared.logging import configure_logging
from sample_app.api_pb2_grpc import add_SampleServiceServicer_to_server
import os
import logging
import grpc
from concurrent import futures


def run(port):
    configure_logging()
    # define grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # add grpc implementation to server
    add_SampleServiceServicer_to_server(SampleServiceImpl(), server)
    # set port
    server.add_insecure_port(f'[::]:{port}')
    # start
    server.start()
    logging.info(f"started server, {port}")
    server.wait_for_termination()
    logging.info("killing server")

if __name__ == '__main__':
    PORT = os.environ.get("APP_PORT") or "9000"
    run(PORT)
