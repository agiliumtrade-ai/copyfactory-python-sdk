from ..httpClient import HttpClient
from .trading_client import TradingClient
import pytest
from ...models import date
import respx
from httpx import Response
copy_factory_api_url = 'https://trading-api-v1.agiliumtrade.agiliumtrade.ai'
http_client = HttpClient()
trading_client = TradingClient(http_client, 'header.payload.sign')


@pytest.fixture(autouse=True)
async def run_around_tests():
    global http_client
    global trading_client
    http_client = HttpClient()
    trading_client = TradingClient(http_client, 'header.payload.sign')


class TestTradingClient:
    @respx.mock
    @pytest.mark.asyncio
    async def test_resynchronize_copyfactory_account(self):
        rsps = respx.post(f'{copy_factory_api_url}/users/current/accounts/' +
                          '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef/' +
                          'resynchronize?strategyId=ABCD').mock(return_value=Response(200))
        await trading_client.resynchronize('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
                                           ['ABCD'])
        assert rsps.calls[0].request.method == 'POST'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'

    @pytest.mark.asyncio
    async def test_not_resynchronize_account_with_account_token(self):
        """Should not resynchronize account with account token."""
        trading_client = TradingClient(http_client, 'token')
        try:
            await trading_client.resynchronize('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
                                               ['ABCD'])
        except Exception as err:
            assert err.__str__() == 'You can not invoke resynchronize method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_stopouts(self):
        """Should retrieve stopouts."""
        expected = [{
          'reason': 'max-drawdown',
          'stoppedAt': '2020-08-08T07:57:30.328Z',
          'strategy': {
            'id': 'ABCD',
            'name': 'Strategy'
          },
          'reasonDescription': 'total strategy equity drawdown exceeded limit'
        }]
        rsps = respx.get(f'{copy_factory_api_url}/users/current/accounts/' +
                         '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef/' +
                         'stopouts').mock(return_value=Response(200, json=expected))
        stopouts = await trading_client.get_stopouts('0123456789abcdef0123456789abcdef0123456789abcdef' +
                                                     '0123456789abcdef')
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/accounts/' + \
            '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef/stopouts'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert stopouts == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_stopouts_with_account_token(self):
        """Should not retrieve stopouts from API with account token."""
        trading_client = TradingClient(http_client, 'token')
        try:
            await trading_client.get_stopouts('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef')
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_stopouts method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_reset_stopouts(self):
        rsps = respx.post(f'{copy_factory_api_url}/users/current/accounts/' +
                          '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef/' +
                          'strategies-subscribed/ABCD/stopouts/daily-equity/reset').mock(return_value=Response(200))
        await trading_client.reset_stopouts('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
                                            'ABCD', 'daily-equity')
        assert rsps.calls[0].request.method == 'POST'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'

    @pytest.mark.asyncio
    async def test_not_reset_stopouts_with_account_token(self):
        """Should not reset stopout with account token."""
        trading_client = TradingClient(http_client, 'token')
        try:
            await trading_client.reset_stopouts('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
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
        rsps = respx.get(f'{copy_factory_api_url}/users/current/accounts/' +
                         '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef/user-log' +
                         '?offset=10&limit=100&startTime=2020-08-01T00%3A00%3A00.000Z&endTime=2020-0' +
                         '8-10T00%3A00%3A00.000Z').mock(return_value=Response(200, json=expected))
        records = await trading_client.get_user_log('0123456789abcdef0123456789abcdef0123456789abcdef' +
                                                    '0123456789abcdef', date('2020-08-01T00:00:00.000Z'),
                                                    date('2020-08-10T00:00:00.000Z'), 10, 100)
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/accounts/' + \
               '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef/user-log' + \
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
            await trading_client.get_user_log('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef')
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_user_log method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'
