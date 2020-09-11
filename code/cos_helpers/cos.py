from chief_of_state.v1.writeside_pb2 import HandleCommandResponse
from google.protobuf.any_pb2 import Any
from google.protobuf.empty_pb2 import Empty


class CosCommandResponses():
    @staticmethod
    def persist_and_reply(event):
        return CosCommandResponses.event(event)

    @staticmethod
    def reply():
        '''helper method for generating a reply message'''
        return CosCommandResponses.no_event()


    @staticmethod
    def event(event):
        '''helper method for generating an event message'''
        any_event = Any()
        any_event.Pack(event)
        response = HandleCommandResponse(event=any_event)
        return response

    @staticmethod
    def no_event():
        '''helper method for generating a no event message'''
        return HandleCommandResponse(no_event=Empty())
