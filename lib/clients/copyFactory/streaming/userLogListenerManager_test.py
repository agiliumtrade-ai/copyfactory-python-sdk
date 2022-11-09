from ....models import date
from .userLogListenerManager import UserLogListenerManager
from .userLogListener import UserLogListener
from ...domain_client import DomainClient
from ..copyFactory_models import CopyFactoryUserLogMessage
from ...errorHandler import NotFoundException
from mock import MagicMock, patch, AsyncMock
from asyncio import sleep
from typing import List
import pytest

token = 'header.payload.sign'
expected = [{
    'time': '2020-08-08T08:57:30.328Z',
    'level': 'INFO',
    'message': 'message1'
}, {
    'time': '2020-08-08T07:57:30.328Z',
    'level': 'INFO',
    'message': 'message0'
}]

expected2 = [{
    'time': '2020-08-08T10:57:30.328Z',
    'level': 'INFO',
    'message': 'message3'
}, {
    'time': '2020-08-08T09:57:30.328Z',
    'level': 'INFO',
    'message': 'message2'
}]

domain_client = DomainClient(MagicMock(), token)
user_log_listener_manager = UserLogListenerManager(domain_client)
call_stub = MagicMock()
error_stub = MagicMock()
listener = UserLogListener()


@pytest.fixture(autouse=True)
async def run_around_tests():
    global domain_client
    domain_client = DomainClient(MagicMock(), token)
    domain_client.request_copyfactory = AsyncMock()
    global user_log_listener_manager
    user_log_listener_manager = UserLogListenerManager(domain_client)
    global call_stub
    call_stub = MagicMock()
    global error_stub
    error_stub = MagicMock()

    class Listener(UserLogListener):
        async def on_user_log(self, log_event: List[CopyFactoryUserLogMessage]):
            call_stub(log_event)

        async def on_error(self, error: Exception):
            error_stub(error)

    global listener
    listener = Listener()


@pytest.fixture()
async def prepare_strategy_logs():
    async def get_logs_func(arg, arg2):
        if arg == {
            'url': '/users/current/strategies/ABCD/user-log/stream',
            'method': 'GET',
            'params': {
                'startTime': '2020-08-08T00:00:00.000Z',
                'positionId': 'positionId',
                'level': 'DEBUG',
                'limit': 10
            },
            'headers': {
                'auth-token': token
            },
        }:
            await sleep(0.1)
            return expected
        elif arg == {
            'url': '/users/current/strategies/ABCD/user-log/stream',
            'method': 'GET',
            'params': {
                'startTime': '2020-08-08T08:57:30.329Z',
                'positionId': 'positionId',
                'level': 'DEBUG',
                'limit': 10
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

    domain_client.request_copyfactory = AsyncMock(side_effect=get_logs_func)


class TestStrategyLogs:
    @pytest.mark.asyncio
    async def test_add_strategy_listener(self, prepare_strategy_logs):
        """Should add listener."""
        with patch('lib.clients.copyFactory.streaming.userLogListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = user_log_listener_manager.add_strategy_log_listener(
                listener, 'ABCD', date('2020-08-08T00:00:00.000Z'), 'positionId', 'DEBUG', 10)
            await sleep(0.22)
            call_stub.assert_any_call(expected)
            call_stub.assert_any_call(expected2)
            user_log_listener_manager.remove_strategy_log_listener(id)

    @pytest.mark.asyncio
    async def test_remove_strategy_listener(self, prepare_strategy_logs):
        """Should remove listener."""
        with patch('lib.clients.copyFactory.streaming.userLogListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = user_log_listener_manager.add_strategy_log_listener(
                listener, 'ABCD', date('2020-08-08T00:00:00.000Z'), 'positionId', 'DEBUG', 10)
            await sleep(0.11)
            user_log_listener_manager.remove_strategy_log_listener(id)
            await sleep(0.22)
            call_stub.assert_any_call(expected)
            assert call_stub.call_count == 1

    @pytest.mark.asyncio
    async def test_wait_if_error_returned(self):
        """Should wait if error returned."""
        call_count = 0
        error = Exception('test')
        error2 = Exception('test')

        async def get_transaction_func(arg, arg2):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise error
            if call_count == 2:
                raise error2

            if arg == {
                'url': '/users/current/strategies/ABCD/user-log/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T00:00:00.000Z',
                    'positionId': 'positionId',
                    'level': 'DEBUG',
                    'limit': 10
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
        with patch('lib.clients.copyFactory.streaming.userLogListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = user_log_listener_manager.add_strategy_log_listener(
                listener, 'ABCD', date('2020-08-08T00:00:00.000Z'), 'positionId', 'DEBUG', 10)
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 1
            assert call_stub.call_count == 0
            assert error_stub.call_count == 1
            error_stub.assert_any_call(error)
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 2
            assert call_stub.call_count == 0
            assert error_stub.call_count == 2
            error_stub.assert_any_call(error2)
            await sleep(0.2)
            assert domain_client.request_copyfactory.call_count == 3
            assert call_stub.call_count == 0
            await sleep(0.08)
            assert call_stub.call_count == 1
            user_log_listener_manager.remove_strategy_log_listener(id)

    @pytest.mark.asyncio
    async def test_remove_listener_on_not_found_error(self):
        """Should remove listener on not found error."""
        error = NotFoundException('test')

        async def get_logs_func(arg, arg2):
            if arg == {
                'url': '/users/current/strategies/ABCD/user-log/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T00:00:00.000Z',
                    'positionId': 'positionId',
                    'level': 'DEBUG',
                    'limit': 10
                },
                'headers': {
                    'auth-token': token
                },
            }:
                await sleep(0.1)
                return expected
            elif arg == {
                'url': '/users/current/strategies/ABCD/user-log/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T08:57:30.329Z',
                    'positionId': 'positionId',
                    'level': 'DEBUG',
                    'limit': 10
                },
                'headers': {
                    'auth-token': token
                },
            }:
                await sleep(0.1)
                raise error

        domain_client.request_copyfactory = AsyncMock(side_effect=get_logs_func)
        with patch('lib.clients.copyFactory.streaming.userLogListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = user_log_listener_manager.add_strategy_log_listener(
                listener, 'ABCD', date('2020-08-08T00:00:00.000Z'), 'positionId', 'DEBUG', 10)
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
            error_stub.assert_called_once()
            error_stub.assert_called_with(error)
            user_log_listener_manager.remove_strategy_log_listener(id)


@pytest.fixture()
async def prepare_subscriber_logs():
    async def get_logs_func(arg, arg2):
        if arg == {
            'url': '/users/current/subscribers/accountId/user-log/stream',
            'method': 'GET',
            'params': {
                'startTime': '2020-08-08T00:00:00.000Z',
                'strategyId': 'strategyId',
                'positionId': 'positionId',
                'level': 'DEBUG',
                'limit': 10
            },
            'headers': {
                'auth-token': token
            },
        }:
            await sleep(0.1)
            return expected
        elif arg == {
            'url': '/users/current/subscribers/accountId/user-log/stream',
            'method': 'GET',
            'params': {
                'startTime': '2020-08-08T08:57:30.329Z',
                'strategyId': 'strategyId',
                'positionId': 'positionId',
                'level': 'DEBUG',
                'limit': 10
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

    domain_client.request_copyfactory = AsyncMock(side_effect=get_logs_func)


class TestSubscriberTransactions:
    @pytest.mark.asyncio
    async def test_add_subscriber_listener(self, prepare_subscriber_logs):
        """Should add listener."""
        with patch('lib.clients.copyFactory.streaming.userLogListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = user_log_listener_manager.add_subscriber_log_listener(
                listener, 'accountId', date('2020-08-08T00:00:00.000Z'), 'strategyId', 'positionId', 'DEBUG', 10)
            await sleep(0.22)
            call_stub.assert_any_call(expected)
            call_stub.assert_any_call(expected2)
            user_log_listener_manager.remove_subscriber_log_listener(id)

    @pytest.mark.asyncio
    async def test_remove_strategy_listener(self, prepare_subscriber_logs):
        """Should remove listener."""
        with patch('lib.clients.copyFactory.streaming.userLogListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = user_log_listener_manager.add_subscriber_log_listener(
                listener, 'accountId', date('2020-08-08T00:00:00.000Z'), 'strategyId', 'positionId', 'DEBUG', 10)
            await sleep(0.11)
            user_log_listener_manager.remove_subscriber_log_listener(id)
            await sleep(0.22)
            call_stub.assert_any_call(expected)
            assert call_stub.call_count == 1

    @pytest.mark.asyncio
    async def test_wait_if_error_returned(self):
        """Should wait if error returned."""
        call_count = 0
        error = Exception('test')
        error2 = Exception('test')

        async def get_transaction_func(arg, arg2):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise error
            if call_count == 2:
                raise error2

            if arg == {
                'url': '/users/current/subscribers/accountId/user-log/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T00:00:00.000Z',
                    'strategyId': 'strategyId',
                    'positionId': 'positionId',
                    'level': 'DEBUG',
                    'limit': 10
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
        with patch('lib.clients.copyFactory.streaming.userLogListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = user_log_listener_manager.add_subscriber_log_listener(
                listener, 'accountId', date('2020-08-08T00:00:00.000Z'), 'strategyId', 'positionId', 'DEBUG', 10)
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 1
            assert call_stub.call_count == 0
            assert error_stub.call_count == 1
            error_stub.assert_any_call(error)
            await sleep(0.06)
            assert domain_client.request_copyfactory.call_count == 2
            assert call_stub.call_count == 0
            assert error_stub.call_count == 2
            error_stub.assert_any_call(error2)
            await sleep(0.2)
            assert domain_client.request_copyfactory.call_count == 3
            assert call_stub.call_count == 0
            await sleep(0.08)
            assert call_stub.call_count == 1
            user_log_listener_manager.remove_subscriber_log_listener(id)

    @pytest.mark.asyncio
    async def test_remove_listener_on_not_found_error(self):
        """Should remove listener on not found error."""
        error = NotFoundException('test')

        async def get_logs_func(arg, arg2):
            if arg == {
                'url': '/users/current/subscribers/accountId/user-log/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T00:00:00.000Z',
                    'strategyId': 'strategyId',
                    'positionId': 'positionId',
                    'level': 'DEBUG',
                    'limit': 10
                },
                'headers': {
                    'auth-token': token
                },
            }:
                await sleep(0.1)
                return expected
            elif arg == {
                'url': '/users/current/subscribers/accountId/user-log/stream',
                'method': 'GET',
                'params': {
                    'startTime': '2020-08-08T08:57:30.329Z',
                    'strategyId': 'strategyId',
                    'positionId': 'positionId',
                    'level': 'DEBUG',
                    'limit': 10
                },
                'headers': {
                    'auth-token': token
                },
            }:
                await sleep(0.1)
                raise error

        domain_client.request_copyfactory = AsyncMock(side_effect=get_logs_func)
        with patch('lib.clients.copyFactory.streaming.userLogListenerManager.asyncio.sleep',
                   new=lambda x: sleep(x / 10)):
            id = user_log_listener_manager.add_subscriber_log_listener(
                listener, 'accountId', date('2020-08-08T00:00:00.000Z'), 'strategyId', 'positionId', 'DEBUG', 10)
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
            error_stub.assert_called_once()
            error_stub.assert_called_with(error)
            user_log_listener_manager.remove_subscriber_log_listener(id)
