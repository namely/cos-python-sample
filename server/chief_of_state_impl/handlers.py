from sample_app.api_pb2 import AppendRequest, GetRequest
from sample_app.events_pb2 import AppendEvent
from sample_app.state_pb2 import State
from google.protobuf.any_pb2 import Any
from chief_of_state.writeside_pb2 import (PersistAndReply, PersistAndReply, Reply)
from chief_of_state_impl.cos_helpers import CosHelpers


class CommandHandler():
    @staticmethod
    def handle_command(command, current_state, meta):
        '''
        general handler that matches on command type url and runs
        appropriate handler method
        '''

        if (command.command.type.contains("AppendRequest")):
            return _handle_command_append(command, current_state, meta)

        elif (command.command.type.contains("GetRequest")):
            return CosHelpers.reply()

        else:
            # TODO: throw error for unknown type url
            return CosHelpers.reply()

    @staticmethod
    def _handle_command_append(command, current_state, meta):
        '''validate AppendRequest and produce an Event'''
        # unpack inner command/event
        real_command = command.Unpack(AppendRequest)
        real_current_state = current_state.Unpack(State)

        # do validation
        assert real_command.id == real_current_state.id, "mismatched ids"
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
