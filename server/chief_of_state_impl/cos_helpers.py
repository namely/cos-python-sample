from chief_of_state.writeside_pb2 import (PersistAndReply, Reply, HandleEventResponse)
from chief_of_state.writeside_pb2 import HandleCommandResponse


class CosHelpers():
    @staticmethod
    def persist_and_reply(event):
        # return event to be persisted
        any_event = Any()
        any_event.Pack(event)

        persist_and_reply = PersistAndReply()
        persist_and_reply.event = any_event

        response = HandleCommandResponse(
            persist_and_reply = persist_and_reply
        )

        return response

    @staticmethod
    def reply():
        return HandleCommandResponse(
            reply=Reply()
        )
