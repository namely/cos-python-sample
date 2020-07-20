from concurrent import futures
import logging
import grpc
import sys
from google.protobuf.any_pb2 import Any
from chief_of_state.writeside_pb2_grpc import WriteSideHandlerServiceServicer
from chief_of_state.writeside_pb2_grpc import add_WriteSideHandlerServiceServicer_to_server
from chief_of_state.writeside_pb2 import (PersistAndReply, PersistAndReply, Reply, HandleCommandRequest, HandleEventRequest)
from .validation import StatefulValidation
from .handlers import CommandHandler, EventHandler
from google.protobuf.json_format import MessageToJson


logger = logging.getLogger(__name__)

class WriteSideHandlerImpl(WriteSideHandlerServiceServicer):



    def HandleCommand(self, request, context):
        logger.debug("begin WriteSideHandlerImpl.HandleCommand")
        assert isinstance(request, HandleCommandRequest)

        # do stateful validation
        # StatefulValidation.validate(request)

        # create event from request
        response = CommandHandler.handle_command(
            command = request.command,
            current_state = request.current_state,
            meta = request.meta
        )

        logger.debug(MessageToJson(response))

        return response


    def HandleEvent(self, request, context):
        assert isinstance(request, HandleEventRequest)

        # given event and prior state, build a new state
        # this should never fail!
        response = EventHandler.handle_event(
            event = request.event,
            current_state = request.current_state,
            meta = request.meta
        )

        logger.debug(MessageToJson(response))

        return response


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def run(port):
    configure_logging()
    logging.info("starting server")
    print("starting server...")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    add_WriteSideHandlerServiceServicer_to_server(WriteSideHandlerImpl(), server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

    logging.info("killing server")
