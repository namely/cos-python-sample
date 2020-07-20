from sample_app.api_pb2 import AppendRequest, GetRequest, CreateRequest
from sample_app.events_pb2 import AppendEvent, CreateEvent
from sample_app.state_pb2 import State
from google.protobuf.any_pb2 import Any
from chief_of_state.writeside_pb2 import PersistAndReply, PersistAndReply, Reply
from write_handler_impl.cos_helpers import CosHelpers
from google.protobuf.json_format import MessageToJson
import logging

logger = logging.getLogger(__name__)


class CommandHandler():
    @staticmethod
    def handle_command(command, current_state, meta):
        '''
        general handler that matches on command type url and runs
        appropriate handler method
        '''
        logger.debug("begin handle_command")
        logger.debug(MessageToJson(command))

        if ("CreateRequest" in command.type_url):
            return CommandHandler._handle_create(
                command = command,
                current_state = current_state,
                meta = meta
            )

        elif ("AppendRequest" in command.type_url):
            return CommandHandler._handle_append(
                command = command,
                current_state = current_state,
                meta = meta
            )

        elif ("GetRequest" in command.type_url):
            return CosHelpers.reply()

        else:
            raise Exception(f"unknown type {command.type_url}")

    @staticmethod
    def _handle_create(command, current_state, meta):
        logger.debug("HANDLE CREATE COMMAND")
        real_command = CreateRequest()
        command.Unpack(real_command)

        real_current_state = State()
        current_state.Unpack(real_current_state)

        assert not real_current_state.id, f'id already exists {real_current_state.id}'

        event = CreateEvent(id=real_command.id)
        output = CosHelpers.persist_and_reply(event)
        logger.debug(MessageToJson(output))

        return output

    @staticmethod
    def _handle_append(command, current_state, meta):
        '''validate AppendRequest and produce an Event'''
        # unpack inner command/event
        real_command = AppendRequest()
        command.Unpack(real_command)

        real_current_state = State()
        current_state.Unpack(real_current_state)

        # do validation
        assert isinstance(real_command, AppendRequest), 'unpack event failed'
        assert isinstance(real_current_state, State), 'unpack state failed'
        if real_current_state.id:
            assert real_command.id == real_current_state.id, f"mismatched ids, {real_command.id} and {real_current_state.id}"
        assert not real_command.append in real_current_state.values, f"duplicate value {real_command.append}"

        # make event
        event = AppendEvent()
        event.id = real_command.id
        event.appended = real_command.append

        return CosHelpers.persist_and_reply(event)


class EventHandler():
    @staticmethod
    def handle_event(event, current_state, meta):
        # build new state
        new_state = State.CopyFrom(current_state)
        new_state.values.append(event.appended)

        # create return
        any_new_state = Any()
        any_new_state.Pack(new_state)

        response = HandleEventResponse()
        response.resulting_state = any_new_state

        return response
