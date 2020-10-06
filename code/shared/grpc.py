import grpc
from grpc import StatusCode
from google.protobuf.message import Message
import logging
import signal
import time

logger = logging.getLogger(__name__)

def get_channel(host, port):
    return grpc.insecure_channel(f'{host}:{port}')


def validate(condition, error_message:str = "", error_code:StatusCode = StatusCode.INVALID_ARGUMENT):
    '''validate or return error message'''

    def _validate(context: grpc.ServicerContext):
        if not condition:
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
