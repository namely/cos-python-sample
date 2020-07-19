from concurrent import futures
import logging
import grpc
import app.api_pb2_grpc
from google.protobuf.any_pb2 import Any
from chief_of_state.writeside_pb2_grpc import WriteSideHandlerServiceServicer
from chief_of_state.writeside_pb2_grpc import add_WriteSideHandlerServiceServicer_to_server
from chief_of_state.writeside_pb2 import (PersistAndReply, PersistAndReply, Reply)
from .validation import StatefulValidation
from .handlers import CommandHandler, EventHandler


class WriteSideHandlerImpl(WriteSideHandlerServiceServicer):

    def HandleCommand(self, request, context):
        # do stateful validation
        StatefulValidation.validate(request)

        # create event from request
        response = CommandHandler.handle_command(
            command = request.command,
            current_state = request.current_state,
            meta = request.meta
        )

        return response


    def HandleEvent(self, request, context):
        # given event and prior state, build a new state
        # this should never fail!
        new_state = EventHandler.handle_event(
            event = request.event,
            current_state = request.current_state,
            meta = request.meta
        )

        # create return
        any_new_state = Any()
        any_new_state.Pack(new_state)

        response = HandleEventResponse()
        response.resulting_state = any_new_state

        return response


def run(port):
    logging.basicConfig()
    logging.info("starting server")
    print("starting server...")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    add_WriteSideHandlerServiceServicer_to_server(WriteSideHandlerImpl(), server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

    logging.info("killing server")
