from write_handler_impl.service import WriteSideHandlerImpl
from chief_of_state.v1.writeside_pb2_grpc import add_WriteSideHandlerServiceServicer_to_server
from shared.logging import configure_logging
from shared.grpc import ServerHelper
import os
import logging
import time
import grpc
from concurrent import futures

from jaeger_client import Config
import opentracing
from grpc_opentracing import open_tracing_server_interceptor
from grpc_opentracing.grpcext import intercept_server


def get_tracer(service_name):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': os.environ.get("TRACE_HOST") or 'tracer',
                'reporting_port': os.environ.get("TRACE_PORT") or '5775',
            },
            'logging': True,
        },
        service_name=service_name,
        validate=True,
    )

    return config.initialize_tracer()


def intercept_grpc_server(server, tracer):
    tracer_interceptor = open_tracing_server_interceptor(tracer)
    new_server = intercept_server(server, tracer_interceptor)
    return new_server

def run(port):

    configure_logging()

    tracer = get_tracer('write-handler')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = intercept_grpc_server(server, tracer)

    add_WriteSideHandlerServiceServicer_to_server(WriteSideHandlerImpl(), server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()

    logging.info(f"started server, {port}")

    ServerHelper().await_termination()
    logging.info("killing server")
    time.sleep(2)
    tracer.close()
    time.sleep(2)

if __name__ == '__main__':
    PORT = os.environ.get("APP_PORT") or "9000"
    run(PORT)
