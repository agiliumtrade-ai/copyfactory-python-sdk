from ....models import date
from .transactionListenerManager import TransactionListenerManager
from .transactionListener import TransactionListener
from ...domain_client import DomainClient
from ..copyFactory_models import CopyFactoryTransaction
from ...errorHandler import NotFoundException
from mock import MagicMock, patch, AsyncMock
from asyncio import sleep
from typing import List
import pytest

token = 'header.payload.sign'
expected = [{
    'id': '64664661:close',
    'type': 'DEAL_TYPE_SELL',
    'time': '2020-08-08T08:57:30.328Z'
}, {
    'id': '64664660:close',
    'type': 'DEAL_TYPE_SELL',
    'time': '2020-08-08T07:57:30.328Z'
}]

expected2 = [{
    'id': '64664663:close',
    'type': 'DEAL_TYPE_SELL',
    'time': '2020-08-08T10:57:30.328Z'
}, {
    'id': '64664662:close',
    'type': 'DEAL_TYPE_SELL',
    'time': '2020-08-08T09:57:30.328Z'
}]
domain_client = DomainClient(MagicMock(), token)
transaction_listener_manager = TransactionListenerManager(domain_client)
call_stub = MagicMock()
listener = TransactionListener()


@pytest.fixture(autouse=True)
async def run_around_tests():
    global domain_client
    domain_client = DomainClient(MagicMock(), token)
    global transaction_listener_manager
    transaction_listener_manager = TransactionListenerManager(domain_client)
    global call_stub
    call_stub = MagicMock()

    class Listener(TransactionListener):
        async def on_transaction(self, transaction_event: List[CopyFactoryTransaction]):
            call_stub(transaction_event)

    global listener
    listener = Listener()


@pytest.fixture()
async def prepare_strategy_transactions():
    async def get_transactions_func(arg, arg2):
        if arg == {
            'url': '/users/current/strategies/ABCD/transactions/stream',
            'method': 'GET',
            'params': {
                'startTime': '2020-08-08T00:00:00.000Z',
                'limit': 1000
            },
            'headers': {
                'auth-token': token
            },
        }:
            await sleep(0.1)
            return expected
        elif arg == {
            'url': '/users/current/strategies/ABCD/transactions/stream',
            'method': 'GET',
            'params': {
                'startTime': '2020-08-08T08:57:30.329Z',
                'limit': 1000
            },
            'headers': {
                'auth-token': token
            },
        }:
            await sleep(0.1)
            return expected2
        else:
            await sleep(0.1)
            return []

    domain_client.request_copyfactory = AsyncMock(side_effect=get_transactions_func)


class TestStrategyTransactions:
    @pytest.mark.asyncio
    async def test_add_strategy_listener(self, prepare_strategy_transactions):
        """Should add listener."""
        with patch('lib.clients.copyFactory.streaming.transactionListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = transaction_listener_manager.add_strategy_transaction_listener(listener, 'ABCD',
                                                                                date('2020-08-08T00:00:00.000Z'))
            await sleep(0.22)
            call_stub.assert_any_call(expected)
            call_stub.assert_any_call(expected2)
            transaction_listener_manager.remove_strategy_transaction_listener(id)

    @pytest.mark.asyncio
    async def test_remove_strategy_listener(self, prepare_strategy_transactions):
        """Should remove listener."""
        with patch('lib.clients.copyFactory.streaming.transactionListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = transaction_listener_manager.add_strategy_transaction_listener(listener, 'ABCD',
                                                                                date('2020-08-08T00:00:00.000Z'))
            await sleep(0.08)
            transaction_listener_manager.remove_strategy_transaction_listener(id)
            await sleep(0.22)
            call_stub.assert_any_call(expected)
            assert call_stub.call_count == 1

    @pytest.mark.asyncio
    async def test_wait_if_error_returned(self):
        """Should wait if error returned."""
        call_count = 0

        async def get_transaction_func(arg, arg2):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception('test')

            if arg == {
                'url': '/users/current/strategies/ABCD/transactions/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T00:00:00.000Z',
                    'limit': 1000
                },
                'headers': {
                    'auth-token': token
                },
            }:
                await sleep(0.05)
                return expected
            else:
                await sleep(0.5)
                return []

        domain_client.request_copyfactory = AsyncMock(side_effect=get_transaction_func)
        with patch('lib.clients.copyFactory.streaming.transactionListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = transaction_listener_manager.add_strategy_transaction_listener(listener, 'ABCD',
                                                                                date('2020-08-08T00:00:00.000Z'))
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 1
            assert call_stub.call_count == 0
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 2
            assert call_stub.call_count == 0
            await sleep(0.2)
            assert domain_client.request_copyfactory.call_count == 3
            assert call_stub.call_count == 0
            await sleep(0.08)
            assert call_stub.call_count == 1
            transaction_listener_manager.remove_strategy_transaction_listener(id)

    @pytest.mark.asyncio
    async def test_remove_listener_on_not_found_error(self):
        """Should remove listener on not found error."""

        async def get_transactions_func(arg, arg2):
            if arg == {
                'url': '/users/current/strategies/ABCD/transactions/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T00:00:00.000Z',
                    'limit': 1000
                },
                'headers': {
                    'auth-token': token
                },
            }:
                await sleep(0.1)
                return expected
            elif arg == {
                'url': '/users/current/strategies/ABCD/transactions/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T08:57:30.329Z',
                    'limit': 1000
                },
                'headers': {
                    'auth-token': token
                },
            }:
                await sleep(0.1)
                raise NotFoundException('test')

        domain_client.request_copyfactory = AsyncMock(side_effect=get_transactions_func)
        with patch('lib.clients.copyFactory.streaming.transactionListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = transaction_listener_manager.add_strategy_transaction_listener(listener, 'ABCD',
                                                                                date('2020-08-08T00:00:00.000Z'))
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 1
            assert call_stub.call_count == 0
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 2
            assert call_stub.call_count == 1
            await sleep(0.2)
            assert domain_client.request_copyfactory.call_count == 2
            assert call_stub.call_count == 1
            await sleep(0.08)
            assert call_stub.call_count == 1
            transaction_listener_manager.remove_strategy_transaction_listener(id)


@pytest.fixture()
async def prepare_subscriber_transactions():
    async def get_transactions_func(arg, arg2):
        if arg == {
            'url': '/users/current/subscribers/accountId/transactions/stream',
            'method': 'GET',
            'params': {
                'startTime': '2020-08-08T00:00:00.000Z',
                'limit': 1000
            },
            'headers': {
                'auth-token': token
            },
        }:
            await sleep(0.1)
            return expected
        elif arg == {
            'url': '/users/current/subscribers/accountId/transactions/stream',
            'method': 'GET',
            'params': {
                'startTime': '2020-08-08T08:57:30.329Z',
                'limit': 1000
            },
            'headers': {
                'auth-token': token
            },
        }:
            await sleep(0.1)
            return expected2
        else:
            await sleep(0.1)
            return []

    domain_client.request_copyfactory = AsyncMock(side_effect=get_transactions_func)


class TestSubscriberTransactions:
    @pytest.mark.asyncio
    async def test_add_subscriber_listener(self, prepare_subscriber_transactions):
        """Should add listener."""
        with patch('lib.clients.copyFactory.streaming.transactionListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = transaction_listener_manager.add_subscriber_transaction_listener(listener, 'accountId',
                                                                                  date('2020-08-08T00:00:00.000Z'))
            await sleep(0.22)
            call_stub.assert_any_call(expected)
            call_stub.assert_any_call(expected2)
            transaction_listener_manager.remove_subscriber_transaction_listener(id)

    @pytest.mark.asyncio
    async def test_remove_strategy_listener(self, prepare_subscriber_transactions):
        """Should remove listener."""
        with patch('lib.clients.copyFactory.streaming.transactionListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = transaction_listener_manager.add_subscriber_transaction_listener(listener, 'accountId',
                                                                                  date('2020-08-08T00:00:00.000Z'))
            await sleep(0.08)
            transaction_listener_manager.remove_subscriber_transaction_listener(id)
            await sleep(0.22)
            call_stub.assert_any_call(expected)
            assert call_stub.call_count == 1

    @pytest.mark.asyncio
    async def test_wait_if_error_returned(self):
        """Should wait if error returned."""
        call_count = 0

        async def get_transaction_func(arg, arg2):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception('test')

            if arg == {
                'url': '/users/current/subscribers/accountId/transactions/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T00:00:00.000Z',
                    'limit': 1000
                },
                'headers': {
                    'auth-token': token
                },
            }:
                await sleep(0.05)
                return expected
            else:
                await sleep(0.5)
                return []

        domain_client.request_copyfactory = AsyncMock(side_effect=get_transaction_func)
        with patch('lib.clients.copyFactory.streaming.transactionListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = transaction_listener_manager.add_subscriber_transaction_listener(listener, 'accountId',
                                                                                  date('2020-08-08T00:00:00.000Z'))
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 1
            assert call_stub.call_count == 0
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 2
            assert call_stub.call_count == 0
            await sleep(0.2)
            assert domain_client.request_copyfactory.call_count == 3
            assert call_stub.call_count == 0
            await sleep(0.08)
            assert call_stub.call_count == 1
            transaction_listener_manager.remove_subscriber_transaction_listener(id)

    @pytest.mark.asyncio
    async def test_remove_listener_on_not_found_error(self):
        """Should remove listener on not found error."""

        async def get_transactions_func(arg, arg2):
            if arg == {
                'url': '/users/current/subscribers/accountId/transactions/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T00:00:00.000Z',
                    'limit': 1000
                },
                'headers': {
                    'auth-token': token
                },
            }:
                await sleep(0.1)
                return expected
            elif arg == {
                'url': '/users/current/subscribers/accountId/transactions/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T08:57:30.329Z',
                    'limit': 1000
                },
                'headers': {
                    'auth-token': token
                },
            }:
                await sleep(0.1)
                raise NotFoundException('test')

        domain_client.request_copyfactory = AsyncMock(side_effect=get_transactions_func)
        with patch('lib.clients.copyFactory.streaming.transactionListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = transaction_listener_manager.add_subscriber_transaction_listener(listener, 'accountId',
                                                                                  date('2020-08-08T00:00:00.000Z'))
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 1
            assert call_stub.call_count == 0
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 2
            assert call_stub.call_count == 1
            await sleep(0.2)
            assert domain_client.request_copyfactory.call_count == 2
            assert call_stub.call_count == 1
            await sleep(0.08)
            assert call_stub.call_count == 1
            transaction_listener_manager.remove_strategy_transaction_listener(id)
