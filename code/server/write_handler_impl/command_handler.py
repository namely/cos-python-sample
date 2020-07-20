from sample_app.api_pb2 import AppendRequest, GetRequest, CreateRequest
from sample_app.events_pb2 import AppendEvent, CreateEvent
from sample_app.state_pb2 import State
from chief_of_state.writeside_pb2 import PersistAndReply, PersistAndReply, Reply, HandleEventResponse
from cos_helpers.cos import CosEventReplyTypes
from cos_helpers.proto import ProtoHelper
import logging


logger = logging.getLogger(__name__)

class CommandHandler():

    @staticmethod
    def handle_command(command, current_state, meta):
        '''
        general command handler that matches on command type url
        and runs appropriate handler method
        '''
        logger.debug(f"CommandHandler.handle_command")

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
            return CosEventReplyTypes.reply()

        else:
            raise Exception(f"unknown type {command.type_url}")


    @staticmethod
    def _handle_create(command, current_state, meta):
        '''validate CreateCommand and produce Event'''

        logger.debug("CommandHandler._handle_create")

        real_command = ProtoHelper.unpack_any(command, CreateRequest)
        real_current_state = ProtoHelper.unpack_any(current_state, State)

        assert real_command.id, "ID required"

        event = CreateEvent(id=real_command.id)
        output = CosEventReplyTypes.persist_and_reply(event)

        return output


    @staticmethod
    def _handle_append(command, current_state, meta):
        '''validate AppendRequest and produce an Event'''

        logger.debug("CommandHandler._handle_append")

        # unpack inner command/event
        real_command = ProtoHelper.unpack_any(command, AppendRequest)
        real_current_state = ProtoHelper.unpack_any(current_state, State)

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

        return CosEventReplyTypes.persist_and_reply(event)