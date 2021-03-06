import grpc
from grpc import StatusCode, RpcError
from grpc_status import rpc_status
from google.protobuf import any_pb2
from google.rpc import code_pb2, status_pb2, error_details_pb2
import logging
import signal
import time
from grpc_opentracing import open_tracing_server_interceptor, open_tracing_client_interceptor
from grpc_opentracing.grpcext import intercept_server, intercept_channel
from jaeger_client import Config
import opentracing
import os
from shared import proto

logger = logging.getLogger(__name__)

def get_channel(host, port, enable_tracing=False):
    channel = grpc.insecure_channel(f'{host}:{port}')
    if enable_tracing:
        tracer_interceptor = open_tracing_client_interceptor(opentracing.global_tracer())
        channel = intercept_channel(channel, tracer_interceptor)
    return channel


def validate(condition, error_message:str = "", error_code:StatusCode = StatusCode.INVALID_ARGUMENT, field_name = None):
    '''validate or return error message'''

    def _validate(context: grpc.ServicerContext):
        if not condition:

            if field_name:
                logger.warn(f"validation failed, field: {field_name}, error: {error_message}")

                detail = error_details_pb2.BadRequest(
                    field_violations = [
                        error_details_pb2.BadRequest.FieldViolation(
                            field = field_name,
                            description = error_message
                        )
                    ]
                )

                status = status_pb2.Status(
                    code=error_code.value[0],
                    message="validation failed",
                    details=[proto.pack_any(detail)]
                )

                # abort with this status
                output_status = rpc_status.to_status(status)
                context.abort_with_status(output_status)

            else:
                logger.warn(f"validation failed, {error_message}")
                context.abort(code=error_code, details=error_message)

    return _validate



class ServerHelper:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

    def await_termination(self):
        while not self.kill_now:
            time.sleep(1)


def get_tracer(service_name):
    config = Config(
        config={
            'logging': False,
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': os.environ.get("TRACE_HOST") or 'tracer',
                'reporting_port': os.environ.get("TRACE_PORT") or '5775',
            },
            'propagation': 'b3',
            'logging': False,
            'reporter_batch_size': 1,
        },
        service_name=service_name,
        validate=True,
    )

    return config.initialize_tracer()


def intercept_grpc_server(server, tracer):
    tracer_interceptor = open_tracing_server_interceptor(tracer)
    new_server = intercept_server(server, tracer_interceptor)
    return new_server

# activates the provided span on the global tracer
def active_global_tracer_span(span):
    opentracing.global_tracer().scope_manager.activate(span, True)
