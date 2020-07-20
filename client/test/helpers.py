import grpc
from google.protobuf.any_pb2 import Any

def get_channel(host, port):
    return grpc.insecure_channel(f'{host}:{port}')

def pack_any(msg):
    any_message = Any()
    any_message.Pack(msg)
    return any_message


def unpack_any(any_message, cls):
    output = cls()
    any_message.Unpack(output)
    return output
