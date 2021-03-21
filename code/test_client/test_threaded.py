from google.protobuf.empty_pb2 import Empty
from uuid import uuid4
import logging
import grpc
from grpc import StatusCode, RpcError

from banking_app.api_pb2_grpc import BankAccountServiceStub
from banking_app.api_pb2 import *
from banking_app.state_pb2 import BankAccount

from shared.grpc import get_channel
from shared.proto import *

logger = logging.getLogger("banking-app")

class TestApi():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port, True)
        stub = BankAccountServiceStub(channel)

        # create and do transactions against many accounts
        balances = {}

        for _ in range(10):
            id = TestApi._open(stub)
            balances[id] = 200

        for id in balances.keys():
            TestApi._debit(stub, id, balances)

        for id in balances.keys():
            TestApi._credit(stub, id, balances)

        for id in balances.keys():
            TestApi._get(stub, id, balances)

    @staticmethod
    def threaded_process(channel, num_credits, account_owner, starting_balance):
        # open an account
        cmd = OpenAccountRequest(account_owner=account_owner, balance=starting_balance)
        response = stub.OpenAccount(cmd)
        assert isinstance(response, ApiResponse)
        account_id = response.account.account_id
        logger.debug(f"created account {account_id}")

        # debit the account in a loop
        for _ in range(num_credits):
            logger.debug(f"credit account {id}")
            request = CreditAccountRequest(account_id=account_id, amount=1)
            response = stub.CreditAccount(request)
            assert isinstance(response, ApiResponse)
            assert response.account.account_id==id

        logger.debug(f"finished testing account {account_id}")