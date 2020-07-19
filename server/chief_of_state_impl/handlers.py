from app.api_pb2 import AppendRequest, GetRequest, State, Event
from google.protobuf.any_pb2 import Any
from chief_of_state.writeside_pb2 import (PersistAndReply, PersistAndReply, Reply)
from chief_of_state_impl.cos_helpers import CosHelpers

class CommandHandler():
    @staticmethod
    def handle_command(command, current_state, meta):
        print(type(command))
        print(command)
        return CosHelpers.reply()
        if (command.command.type.contains("AppendRequest")):
            return _handle_command_append(command, current_state, meta)
        elif (command.command.type.contains("GetRequest")):
            return _handle_command_get
        else:
            # TODO: throw error
            return CosHelpers.reply()

    @staticmethod
    def _handle_command_append(command, current_state, meta):
        # unpack inner command/event
        real_command = command.Unpack(AppendRequest)
        real_current_state = current_state.Unpack(State)

        # do validation
        assert real_command.id == real_current_state.id, "mismatched ids"
        assert not real_command.append in real_current_state.values, f"duplicate value {real_command.append}"

        # make event
        event = Event()
        event.id = real_command.id
        event.appended = real_command.append

        return CosHelpers.persist_and_reply(event)

    @staticmethod
    def _handle_command_get(command, current_state, meta):
        return CosHelpers.reply()

    @staticmethod
    def handle_event(event, current_state, meta):
        pass
