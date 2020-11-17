import logging
import uuid
import os
from grpc import StatusCode, ServicerContext
from google.protobuf.any_pb2 import Any
from chief_of_state.v1.service_pb2_grpc import ChiefOfStateServiceStub
from chief_of_state.v1.service_pb2 import *
from banking_app.api_pb2_grpc import BankAccountServiceServicer
from banking_app.state_pb2 import BankAccount
from banking_app.api_pb2 import (
    DebitAccountRequest,
    CreditAccountRequest,
    OpenAccountRequest,
    GetAccountRequest,
    ApiResponse
)

from shared.proto import unpack_any, pack_any, to_json
from shared.grpc import validate, get_channel
from uuid import uuid4
import grpc


logger = logging.getLogger(__name__)


class BankingServiceImpl(BankAccountServiceServicer):
    '''this class implements the BankingService gRPC interface'''

    def OpenAccount(self, request: OpenAccountRequest, context) -> ApiResponse:
        '''handle requests to open an account'''

        logger.info("opening account")

        validate(request.balance >= 200, "minimum balance of 200 required")(context)

        account_id = str(uuid4())
        result = self._cos_process_command(id=account_id, command=request, context=context)
        validate(result is not None, "state was none", StatusCode.INTERNAL)(context)

        return ApiResponse(account=result)


    def DebitAccount(self, request: DebitAccountRequest, context) -> ApiResponse:
        '''handle debit account'''

        logger.info("debiting account")

        validate(request.amount > 0, "amount must be greater than 0")(context)

        result = self._cos_process_command(id=request.account_id, command=request, context=context)
        validate(result is not None, "state was none", StatusCode.INTERNAL)(context)

        return ApiResponse(account=result)


    def CreditAccount(self, request: CreditAccountRequest, context) -> ApiResponse:
        '''handle credit account'''
        logger.info("crediting account")

        validate(request.amount >= 0, "credits must be positive")(context)

        result = self._cos_process_command(id=request.account_id, command=request, context=context)
        validate(result is not None, "state was none", StatusCode.INTERNAL)(context)

        return ApiResponse(account=result)


    def Get(self, request: GetAccountRequest, context: grpc.ServicerContext) -> ApiResponse:
        '''handle get request'''
        logger.info("getting account")
        client = self._get_cos_client()
        command = GetStateRequest()
        command.entity_id=request.account_id

        try:
            result = client.GetState(command)
            validate(result.HasField("state"), "state was none", StatusCode.NOT_FOUND)(context)
            state = self._cos_unpack_state(result.state)
            validate(state is not None, "state was none", StatusCode.NOT_FOUND)(context)

        except grpc.RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                context.abort(code=e.code(), details=e.details())
            else:
                context.abort(code=StatusCode.INTERNAL, details=e.details())

        return ApiResponse(account=state)

    @classmethod
    def get_subject_crn(cls, context):
        for key, value in context.invocation_metadata():
            if key == 'x-namely-subject-crn':
                return value

    @classmethod
    def get_company_uuid(cls, context):
        for key, value in context.invocation_metadata():
            if key == 'x-company-uuid':
                return value

    @classmethod
    def get_service_entity_crn(cls, context):
        for key, value in context.invocation_metadata():
            if key == 'x-namely-process-crn':
                return value

    @classmethod
    def get_on_behalf_of_crn(cls, context):
        for key, value in context.invocation_metadata():
            if key == 'x-namely-on-behalf-of-crn':
                return value

    @classmethod
    def get_impersonator_crn(cls, context):
        for key, value in context.invocation_metadata():
            if key == 'x-namely-impersonator-crn':
                return value

    @classmethod
    def _cos_process_command(cls, id, command, context):
        '''helper method to run process command'''
        logger.debug("begin process_command")
        client = cls._get_cos_client()
        command_any = pack_any(command)

        subject_crn = cls.get_subject_crn(context)
        company_uuid = cls.get_company_uuid(context)
        service_entity_crn = cls.get_service_entity_crn(context)
        on_behalf_of_crn = cls.get_on_behalf_of_crn(context)
        impersonator_crn = cls.get_impersonator_crn(context)

        metadata = [('x-custom-request-uuid', str(uuid4())),
                    ('x-namely-subject-crn', subject_crn),
                    ('x-company-uuid', company_uuid),
                    ('x-namely-process-crn', service_entity_crn),
                    ('x-namely-on-behalf-of-crn', on_behalf_of_crn),
                    ('x-namely-impersonator-crn', impersonator_crn)]

        request = ProcessCommandRequest(entity_id=id, command=command_any)

        try:
            response = client.ProcessCommand(request=request, metadata=metadata)
            return cls._cos_unpack_state(response.state)
        except grpc.RpcError as e:
            context.abort(code=e.code(), details=e.details())
        except Exception as e:
            context.abort(code=StatusCode.INTERNAL, details=str(e))

    @staticmethod
    def _cos_unpack_state(any_state):
        '''return state or None if a proto Empty message'''
        assert isinstance(any_state, Any), 'expecting Any'

        if any_state.type_url.endswith('google.protobuf.Empty'):
            logger.debug('converting google.protobuf.Empty to None')
            return None
        else:
            return unpack_any(any_state, BankAccount)


    @staticmethod
    def _get_cos_client():
        host = os.environ.get("COS_HOST")
        port = os.environ.get("COS_PORT")
        channel = get_channel(host, port, True)
        return ChiefOfStateServiceStub(channel)
