from ..httpClient import HttpClient
from .history_client import HistoryClient
from ...models import date, format_date
from datetime import datetime
import pytest
import respx
from httpx import Response
copy_factory_api_url = 'https://trading-api-v1.agiliumtrade.agiliumtrade.ai'
http_client = HttpClient()
history_client = HistoryClient(http_client, 'header.payload.sign')


@pytest.fixture(autouse=True)
async def run_around_tests():
    global http_client
    global history_client
    http_client = HttpClient()
    history_client = HistoryClient(http_client, 'header.payload.sign')


class TestHistoryClient:
    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_providers_from_api(self):
        """Should retrieve providers from API."""
        expected = [{
            'id': '577f095ab64b4d1710de34f6a28ab3bd',
            'name': 'First Last',
            'strategies': [{
                'id': 'ABCD',
                'name': 'Test strategy'
            }]
        }]

        rsps = respx.get(f'{copy_factory_api_url}/users/current/providers')\
            .mock(return_value=Response(200, json=expected))
        accounts = await history_client.get_providers()
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/providers'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert accounts == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_providers_with_account_token(self):
        """Should not retrieve providers from API with account token."""
        history_client = HistoryClient(http_client, 'token')
        try:
            await history_client.get_providers()
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_providers method, because you have connected with ' + \
                                    'account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_subscribers_from_api(self):
        """Should retrieve subscribers from API."""
        expected = [{
          'id': '577f095ab64b4d1710de34f6a28ab3bd',
          'name': 'First Last',
          'strategies': [{
            'id': 'ABCD',
            'name': 'Test strategy'
          }]
        }]
        rsps = respx.get(f'{copy_factory_api_url}/users/current/subscribers') \
            .mock(return_value=Response(200, json=expected))
        accounts = await history_client.get_subscribers()
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/subscribers'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert accounts == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_subscribers_with_account_token(self):
        """Should not retrieve subscribers from API with account token."""
        history_client = HistoryClient(http_client, 'token')
        try:
            await history_client.get_subscribers()
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_subscribers method, because you have connected with ' + \
                                    'account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_strategies_subscribed_from_api(self):
        """Should retrieve strategies subscribed to from API."""
        expected = [{
            'id': 'ABCD',
            'name': 'Test strategy'
        }]
        rsps = respx.get(f'{copy_factory_api_url}/users/current/strategies-subscribed') \
            .mock(return_value=Response(200, json=expected))
        accounts = await history_client.get_strategies_subscribed()
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/strategies-subscribed'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert accounts == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_strategies_subscribed_to_with_account_token(self):
        """Should not retrieve strategies subscribed to from API with account token."""
        history_client = HistoryClient(http_client, 'token')
        try:
            await history_client.get_strategies_subscribed()
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_strategies_subscribed method, because you have ' +\
                   'connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_provided_strategies_from_api(self):
        """Should retrieve strategies subscribed to from API."""
        expected = [{
            'id': 'ABCD',
            'name': 'Test strategy'
        }]
        rsps = respx.get(f'{copy_factory_api_url}/users/current/provided-strategies') \
            .mock(return_value=Response(200, json=expected))
        accounts = await history_client.get_provided_strategies()
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/provided-strategies'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert accounts == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_provided_strategies_with_account_token(self):
        """Should not retrieve provided strategies from API with account token."""
        history_client = HistoryClient(http_client, 'token')
        try:
            await history_client.get_provided_strategies()
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_provided_strategies method, because you have ' +\
                   'connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_transactions_for_provided_strategies_from_api(self):
        """Should retrieve transactions performed on provided strategies from API."""
        expected = [{
            'id': '64664661:close',
            'type': 'DEAL_TYPE_SELL',
            'time': '2020-08-02T21:01:01.830Z',
            'accountId': '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
            'symbol': 'EURJPY',
            'subscriber': {
                'id': 'subscriberId',
                'name': 'Subscriber'
            },
            'demo': False,
            'provider': {
                'id': 'providerId',
                'name': 'Provider'
            },
            'strategy': {
                'id': 'ABCD'
            },
            'improvement': 0,
            'providerCommission': 0,
            'platformCommission': 0,
            'quantity': -0.04,
            'lotPrice': 117566.08744776,
            'tickPrice': 124.526,
            'amount': -4702.643497910401,
            'commission': -0.14,
            'swap': -0.14,
            'profit': 0.49
        }]
        time_from = datetime.now()
        time_till = datetime.now()
        rsps = respx.get(url__startswith=f'{copy_factory_api_url}/users/current/provided-strategies') \
            .mock(return_value=Response(200, json=expected))
        accounts = await history_client.get_provided_strategies_transactions(time_from, time_till, ['ABCD'],
                                                                             ['subscriberId'], 100, 200)
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/provided-strategies/' \
                                            f'transactions?from={format_date(time_from).replace(":", "%3A")}&' \
                                            f'till={format_date(time_till).replace(":", "%3A")}&strategyId=ABCD&' \
                                            f'subscriberId=subscriberId&offset=100&limit=200'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        expected[0]['time'] = date(expected[0]['time'])
        assert accounts == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_transactions_for_provided_strategies_with_account_token(self):
        """Should not retrieve transactions on provided strategies from API with account token."""
        history_client = HistoryClient(http_client, 'token')
        try:
            await history_client.get_provided_strategies_transactions(datetime.now(), datetime.now())
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_provided_strategies_transactions method, because ' + \
                   'you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_transactions_for_subscribed_strategies_from_api(self):
        """Should retrieve transactions performed on strategies current user is subscribed to from API."""
        expected = [{
            'id': '64664661:close',
            'type': 'DEAL_TYPE_SELL',
            'time': '2020-08-02T21:01:01.830Z',
            'accountId': '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
            'symbol': 'EURJPY',
            'subscriber': {
                'id': 'subscriberId',
                'name': 'Subscriber'
            },
            'demo': False,
            'provider': {
                'id': 'providerId',
                'name': 'Provider'
            },
            'strategy': {
                'id': 'ABCD'
            },
            'improvement': 0,
            'providerCommission': 0,
            'platformCommission': 0,
            'quantity': -0.04,
            'lotPrice': 117566.08744776,
            'tickPrice': 124.526,
            'amount': -4702.643497910401,
            'commission': -0.14,
            'swap': -0.14,
            'profit': 0.49
        }]
        time_from = datetime.now()
        time_till = datetime.now()
        rsps = respx.get(f'{copy_factory_api_url}/users/current/strategies-subscribed/transactions') \
            .mock(return_value=Response(200, json=expected))
        accounts = await history_client.get_strategies_subscribed_transactions(time_from, time_till, ['ABCD'],
                                                                               ['subscriberId'], 100, 200)
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/strategies-subscribed/' \
                                            f'transactions?from={format_date(time_from).replace(":", "%3A")}&' \
                                            f'till={format_date(time_till).replace(":", "%3A")}&strategyId=ABCD&' \
                                            f'providerId=subscriberId&offset=100&limit=200'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        expected[0]['time'] = date(expected[0]['time'])
        assert accounts == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_transactions_for_subscribed_strategies_with_account_token(self):
        """Should not retrieve transactions on strategies subscribed to from API with account token."""
        history_client = HistoryClient(http_client, 'token')
        try:
            await history_client.get_strategies_subscribed_transactions(datetime.now(), datetime.now())
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_strategies_subscribed_transactions method, ' + \
                   'because you have connected with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'
