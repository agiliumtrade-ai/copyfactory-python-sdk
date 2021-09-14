from ..httpClient import HttpClient
from .trading_client import TradingClient
import pytest
from ...models import date, format_date
import respx
import json
from httpx import Response
copy_factory_api_url = 'https://copyfactory-application-history-master-v1.agiliumtrade.agiliumtrade.ai'
http_client = HttpClient()
trading_client = TradingClient(http_client, 'header.payload.sign')


@pytest.fixture(autouse=True)
async def run_around_tests():
    global http_client
    global trading_client
    http_client = HttpClient()
    trading_client = TradingClient(http_client, 'header.payload.sign')


class TestTradingClient:
    @pytest.mark.asyncio
    async def test_generate_signal_id(self):
        """Should generate signal id."""
        assert len(trading_client.generate_signal_id()) == 8

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_external_signal(self):
        """Should update external signal."""
        signal = {
            'symbol': 'EURUSD',
            'type': 'POSITION_TYPE_BUY',
            'time': date('2020-08-24T00:00:00.000Z'),
            'updateTime': date('2020-08-24T00:00:00.000Z'),
            'volume': 1
        }
        rsps = respx.put(f'{copy_factory_api_url}/users/current/strategies/ABCD/external-signals/0123456')\
            .mock(return_value=Response(200))
        await trading_client.update_external_signal('ABCD', '0123456', signal)
        assert rsps.calls[0].request.method == 'PUT'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        signal['time'] = format_date(signal['time'])
        signal['updateTime'] = format_date(signal['updateTime'])
        assert rsps.calls[0].request.content == json.dumps(signal).encode('utf-8')

    @pytest.mark.asyncio
    async def test_not_update_external_signal_with_account_token(self):
        """Should not update external signal with account token."""
        trading_client = TradingClient(http_client, 'token')
        try:
            await trading_client.update_external_signal('ABCD', '0123456', {})
        except Exception as err:
            assert err.__str__() == 'You can not invoke update_external_signal method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_remove_external_signal(self):
        """Should remove external signal."""
        rsps = respx.post(f'{copy_factory_api_url}/users/current/strategies/ABCD/external-signals/0123456/remove')\
            .mock(return_value=Response(200))
        await trading_client.remove_external_signal('ABCD', '0123456', {'time': date('2020-08-24T00:00:00.000Z')})
        assert rsps.calls[0].request.method == 'POST'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert rsps.calls[0].request.content == json.dumps({'time': '2020-08-24T00:00:00.000Z'}).encode('utf-8')

    @pytest.mark.asyncio
    async def test_not_remove_external_signal_with_account_token(self):
        """Should not remove external signal with account token."""
        trading_client = TradingClient(http_client, 'token')
        try:
            await trading_client.remove_external_signal('ABCD', '0123456', {'time': date('2020-08-24T00:00:00.000Z')})
        except Exception as err:
            assert err.__str__() == 'You can not invoke remove_external_signal method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_resynchronize_copyfactory_subscriber(self):
        """Should resynchronize CopyFactory subscriber."""
        rsps = respx.post(f'{copy_factory_api_url}/users/current/subscribers/' +
                          'e8867baa-5ec2-45ae-9930-4d5cea18d0d6/' +
                          'resynchronize?strategyId=ABCD&positionId=0123456').mock(return_value=Response(200))
        await trading_client.resynchronize('e8867baa-5ec2-45ae-9930-4d5cea18d0d6', ['ABCD'], ['0123456'])
        assert rsps.calls[0].request.method == 'POST'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'

    @pytest.mark.asyncio
    async def test_not_resynchronize_account_with_account_token(self):
        """Should not resynchronize CopyFactory subscriber with account token."""
        trading_client = TradingClient(http_client, 'token')
        try:
            await trading_client.resynchronize('e8867baa-5ec2-45ae-9930-4d5cea18d0d6',
                                               ['ABCD'], ['0123456'])
        except Exception as err:
            assert err.__str__() == 'You can not invoke resynchronize method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_signals(self):
        """Should retrieve signals."""
        expected = [{
            'symbol': 'EURUSD',
            'type': 'POSITION_TYPE_BUY',
            'time': '2020-08-24T00:00:00.000Z',
            'closeAfter': '2020-08-24T00:00:00.000Z',
            'volume': 1
        }]
        rsps = respx.get(url__startswith=f'{copy_factory_api_url}/users/current/subscribers/' +
                         'e8867baa-5ec2-45ae-9930-4d5cea18d0d6/signals') \
            .mock(return_value=Response(200, json=expected))
        signals = await trading_client.\
            get_trading_signals('e8867baa-5ec2-45ae-9930-4d5cea18d0d6')
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/subscribers/' + \
            'e8867baa-5ec2-45ae-9930-4d5cea18d0d6/signals'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        expected[0]['time'] = date(expected[0]['time'])
        expected[0]['closeAfter'] = date(expected[0]['closeAfter'])
        assert signals == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_signals_with_account_token(self):
        """Should not retrieve signals with account token."""
        trading_client = TradingClient(http_client, 'token')
        try:
            await trading_client.get_trading_signals('test')
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_signals method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_stopouts(self):
        """Should retrieve stopouts."""
        expected = [{
            'partial': False,
            'reason': 'max-drawdown',
            'stoppedAt': '2020-08-08T07:57:30.328Z',
            'stoppedTill': '2020-08-08T07:57:31.328Z',
            'strategy': {
                'id': 'ABCD',
                'name': 'Strategy'
            },
            'reasonDescription': 'total strategy equity drawdown exceeded limit'
        }]
        rsps = respx.get(f'{copy_factory_api_url}/users/current/subscribers/' +
                         'e8867baa-5ec2-45ae-9930-4d5cea18d0d6/' +
                         'stopouts').mock(return_value=Response(200, json=expected))
        stopouts = await trading_client.get_stopouts('e8867baa-5ec2-45ae-9930-4d5cea18d0d6')
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/subscribers/' + \
            'e8867baa-5ec2-45ae-9930-4d5cea18d0d6/stopouts'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        expected[0]['stoppedAt'] = date(expected[0]['stoppedAt'])
        expected[0]['stoppedTill'] = date(expected[0]['stoppedTill'])
        assert stopouts == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_stopouts_with_account_token(self):
        """Should not retrieve stopouts from API with account token."""
        trading_client = TradingClient(http_client, 'token')
        try:
            await trading_client.get_stopouts('e8867baa-5ec2-45ae-9930-4d5cea18d0d6')
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_stopouts method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_reset_stopouts(self):
        """Should reset stopouts."""
        rsps = respx.post(f'{copy_factory_api_url}/users/current/subscribers/' +
                          'e8867baa-5ec2-45ae-9930-4d5cea18d0d6/' +
                          'subscription-strategies/ABCD/stopouts/daily-equity/reset').mock(return_value=Response(200))
        await trading_client.reset_stopouts('e8867baa-5ec2-45ae-9930-4d5cea18d0d6',
                                            'ABCD', 'daily-equity')
        assert rsps.calls[0].request.method == 'POST'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'

    @pytest.mark.asyncio
    async def test_not_reset_stopouts_with_account_token(self):
        """Should not reset stopouts with account token."""
        trading_client = TradingClient(http_client, 'token')
        try:
            await trading_client.reset_stopouts('e8867baa-5ec2-45ae-9930-4d5cea18d0d6',
                                                'ABCD', 'daily-equity')
        except Exception as err:
            assert err.__str__() == 'You can not invoke reset_stopouts method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_copy_trading_log(self):
        """Should retrieve copy trading user log."""
        expected = [{
          'time': '2020-08-08T07:57:30.328Z',
          'level': 'INFO',
          'message': 'message'
        }]
        rsps = respx.get(f'{copy_factory_api_url}/users/current/subscribers/' +
                         'e8867baa-5ec2-45ae-9930-4d5cea18d0d6/user-log' +
                         '?offset=10&limit=100&startTime=2020-08-01T00%3A00%3A00.000Z&endTime=2020-0' +
                         '8-10T00%3A00%3A00.000Z').mock(return_value=Response(200, json=expected))
        records = await trading_client.get_user_log('e8867baa-5ec2-45ae-9930-4d5cea18d0d6',
                                                    date('2020-08-01T00:00:00.000Z'),
                                                    date('2020-08-10T00:00:00.000Z'), 10, 100)
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/subscribers/' + \
               'e8867baa-5ec2-45ae-9930-4d5cea18d0d6/user-log' + \
               '?offset=10&limit=100&startTime=2020-08-01T00%3A00%3A00.000Z&endTime=2020-08-10T00%3A00%3A00.000Z'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        expected[0]['time'] = date(expected[0]['time'])
        assert records == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_copy_trading_log_with_account_token(self):
        """Should not retrieve copy trading user log from API with account token."""
        trading_client = TradingClient(http_client, 'token')
        try:
            await trading_client.get_user_log('e8867baa-5ec2-45ae-9930-4d5cea18d0d6')
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_user_log method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'
