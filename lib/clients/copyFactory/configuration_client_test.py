from ..httpClient import HttpClient
from .configuration_client import ConfigurationClient
from ...models import date, format_date
import pytest
import json
import respx
from copy import deepcopy
from httpx import Response

copy_factory_api_url = 'https://copyfactory-application-history-master-v1.agiliumtrade.agiliumtrade.ai'
http_client = HttpClient()
copy_factory_client = ConfigurationClient(http_client, 'header.payload.sign')


@pytest.fixture(autouse=True)
async def run_around_tests():
    global http_client
    global copy_factory_client
    http_client = HttpClient()
    copy_factory_client = ConfigurationClient(http_client, 'header.payload.sign')


class TestConfigurationClient:
    @pytest.mark.asyncio
    async def test_generate_account_id(self):
        """Should generate account id."""
        assert len(copy_factory_client.generate_account_id()) == 64

    @respx.mock
    @pytest.mark.asyncio
    async def test_generate_strategy_id(self):
        """Should retrieve CopyFactory accounts from API."""
        expected = {
            'id': 'ABCD'
        }
        rsps = respx.get(f'{copy_factory_api_url}/users/current/configuration/unused-strategy-id')\
            .mock(return_value=Response(200, json=expected))
        id = await copy_factory_client.generate_strategy_id()
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/unused-strategy-id'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert id == expected

    @pytest.mark.asyncio
    async def test_not_generate_strategy_id_with_account_token(self):
        """Should not generate strategy id with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.generate_strategy_id()
        except Exception as err:
            assert err.__str__() == 'You can not invoke generate_strategy_id method, because you have connected ' + \
                   'with account access token. Please use API access token from ' + \
                   'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_strategies_from_api(self):
        """Should retrieve strategies from API."""
        expected = [{
            '_id': 'ABCD',
            'platformCommissionRate': 0.01,
            'name': 'Test strategy',
            'positionLifecycle': 'hedging',
            'accountId': 'e8867baa-5ec2-45ae-9930-4d5cea18d0d6',
            'maxTradeRisk': 0.1,
            'stopOutRisk': {
                'value': 0.4,
                'startTime': '2020-08-24T00:00:00.000Z'
            },
            'riskLimits': [{
                'type': 'monthly',
                'applyTo': 'balance',
                'maxRisk': 0.5,
                'closePositions': False,
                'startTime': '2020-08-24T00:00:01.000Z'
            }],
            'timeSettings': {
                'lifetimeInHours': 192,
                'openingIntervalInMinutes': 5
            }
        }]
        rsps = respx.get(f'{copy_factory_api_url}/users/current/configuration/strategies') \
            .mock(return_value=Response(200, json=expected))
        strategies = await copy_factory_client.get_strategies()
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/strategies'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        expected[0]['stopOutRisk']['startTime'] = date(expected[0]['stopOutRisk']['startTime'])
        expected[0]['riskLimits'][0]['startTime'] = date(expected[0]['riskLimits'][0]['startTime'])
        assert strategies == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_strategies_with_account_token(self):
        """Should not retrieve strategies with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.get_strategies()
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_strategies method, because you have connected with ' + \
                                    'account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_strategy_from_api(self):
        """Should retrieve strategy from API."""
        expected = {
            '_id': 'ABCD',
            'platformCommissionRate': 0.01,
            'name': 'Test strategy',
            'positionLifecycle': 'hedging',
            'accountId': 'e8867baa-5ec2-45ae-9930-4d5cea18d0d6',
            'maxTradeRisk': 0.1,
            'stopOutRisk': {
                'value': 0.4,
                'startTime': '2020-08-24T00:00:00.000Z'
            },
            'riskLimits': [{
                'type': 'monthly',
                'applyTo': 'balance',
                'maxRisk': 0.5,
                'closePositions': False,
                'startTime': '2020-08-24T00:00:01.000Z'
            }],
            'timeSettings': {
                'lifetimeInHours': 192,
                'openingIntervalInMinutes': 5
            }
        }
        rsps = respx.get(f'{copy_factory_api_url}/users/current/configuration/strategies/ABCD') \
            .mock(return_value=Response(200, json=expected))
        strategy = await copy_factory_client.get_strategy('ABCD')
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/strategies/ABCD'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        expected['stopOutRisk']['startTime'] = date(expected['stopOutRisk']['startTime'])
        expected['riskLimits'][0]['startTime'] = date(expected['riskLimits'][0]['startTime'])
        assert strategy == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_strategy_with_account_token(self):
        """Should not retrieve strategy with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.get_strategy('ABCD')
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_strategy method, because you have connected with ' + \
                                    'account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_strategy(self):
        """Should update strategy via API."""
        strategy = {
            'name': 'Test strategy',
            'description': 'Test description',
            'positionLifecycle': 'hedging',
            'maxTradeRisk': 0.1,
            'stopOutRisk': {
                'value': 0.4,
                'startTime': date('2020-08-24T00:00:00.000Z')
            },
            'riskLimits': [{
                'type': 'monthly',
                'applyTo': 'balance',
                'maxRisk': 0.5,
                'closePositions': False,
                'startTime': date('2020-08-24T00:00:01.000Z')
            }],
            'timeSettings': {
                'lifetimeInHours': 192,
                'openingIntervalInMinutes': 5
            }
        }
        json_copy = deepcopy(strategy)
        json_copy['stopOutRisk']['startTime'] = format_date(json_copy['stopOutRisk']['startTime'])
        json_copy['riskLimits'][0]['startTime'] = format_date(json_copy['riskLimits'][0]['startTime'])
        rsps = respx.put(f'{copy_factory_api_url}/users/current/configuration/strategies/ABCD', json=json_copy)\
            .mock(return_value=Response(200))
        await copy_factory_client.update_strategy('ABCD', strategy)
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/strategies/ABCD'
        assert rsps.calls[0].request.method == 'PUT'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert rsps.calls[0].request.content == json.dumps(json_copy).encode('utf-8')

    @pytest.mark.asyncio
    async def test_not_update_strategy_with_account_token(self):
        """Should not update strategy with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.update_strategy('ABCD', {})
        except Exception as err:
            assert err.__str__() == 'You can not invoke update_strategy method, because you have connected with ' + \
                                    'account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_remove_strategy(self):
        """Should remove strategy via API."""
        payload = {'mode': 'preserve'}
        rsps = respx.delete(f'{copy_factory_api_url}/users/current/configuration/strategies/ABCD') \
            .mock(return_value=Response(204))
        await copy_factory_client.remove_strategy('ABCD', payload)
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/strategies/ABCD'
        assert rsps.calls[0].request.method == 'DELETE'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert rsps.calls[0].request.content == json.dumps(payload).encode('utf-8')

    @pytest.mark.asyncio
    async def test_not_remove_strategy_with_account_token(self):
        """Should not remove strategy with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.remove_strategy('ABCD')
        except Exception as err:
            assert err.__str__() == 'You can not invoke remove_strategy method, because you have connected with ' + \
                                    'account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_portfolio_strategies(self):
        """Should retrieve portfolio strategies from API."""
        expected = [{
            '_id': 'ABCD',
            'platformCommissionRate': 0.01,
            'name': 'Test strategy',
            'members': [{
                'strategyId': 'BCDE',
                'stopOutRisk': {
                    'value': 0.4,
                    'startTime': '2020-08-24T00:00:00.000Z'
                },
                'riskLimits': [{
                    'type': 'daily',
                    'startTime': '2020-08-24T00:00:00.000Z'
                }]
            }],
            'maxTradeRisk': 0.1,
            'stopOutRisk': {
                'value': 0.4,
                'startTime': '2020-08-24T00:00:00.000Z'
            }
        }]
        rsps = respx.get(f'{copy_factory_api_url}/users/current/configuration/portfolio-strategies') \
            .mock(return_value=Response(200, json=expected))
        strategies = await copy_factory_client.get_portfolio_strategies()
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/' \
                                            f'portfolio-strategies'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        expected[0]['members'][0]['stopOutRisk']['startTime'] = \
            date(expected[0]['members'][0]['stopOutRisk']['startTime'])
        expected[0]['members'][0]['riskLimits'][0]['startTime'] = \
            date(expected[0]['members'][0]['riskLimits'][0]['startTime'])
        expected[0]['stopOutRisk']['startTime'] = date(expected[0]['stopOutRisk']['startTime'])
        assert strategies == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_portfolio_strategies_with_account_token(self):
        """Should not retrieve portfolio strategies from API with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.get_portfolio_strategies()
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_portfolio_strategies method, because you have connected '\
                                    'with account access token. Please use API access token from '\
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_portfolio_strategy(self):
        """Should retrieve portfolio strategy from API."""
        expected = {
            '_id': 'ABCD',
            'platformCommissionRate': 0.01,
            'name': 'Test strategy',
            'members': [{
                'strategyId': 'BCDE',
                'stopOutRisk': {
                    'value': 0.4,
                    'startTime': '2020-08-24T00:00:00.000Z'
                },
                'riskLimits': [{
                    'type': 'daily',
                    'startTime': '2020-08-24T00:00:00.000Z'
                }]
            }],
            'maxTradeRisk': 0.1,
            'stopOutRisk': {
                'value': 0.4,
                'startTime': '2020-08-24T00:00:00.000Z'
            }
        }
        rsps = respx.get(f'{copy_factory_api_url}/users/current/configuration/portfolio-strategies/ABCD') \
            .mock(return_value=Response(200, json=expected))
        strategies = await copy_factory_client.get_portfolio_strategy('ABCD')
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/' \
                                            f'portfolio-strategies/ABCD'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        expected['members'][0]['stopOutRisk']['startTime'] = \
            date(expected['members'][0]['stopOutRisk']['startTime'])
        expected['members'][0]['riskLimits'][0]['startTime'] = \
            date(expected['members'][0]['riskLimits'][0]['startTime'])
        expected['stopOutRisk']['startTime'] = date(expected['stopOutRisk']['startTime'])
        assert strategies == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_portfolio_strategy_with_account_token(self):
        """Should not retrieve portfolio strategy from API with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.get_portfolio_strategy('ABCD')
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_portfolio_strategy method, because you have connected '\
                                    'with account access token. Please use API access token from '\
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_portfolio_strategy(self):
        """Should update portfolio strategy via API."""
        strategy = {
            'name': 'Test strategy',
            'members': [{
                'strategyId': 'BCDE'
            }],
            'maxTradeRisk': 0.1,
            'stopOutRisk': {
                'value': 0.4,
                'startTime': '2020-08-24T00:00:00.000Z'
            }
        }
        rsps = respx.put(f'{copy_factory_api_url}/users/current/configuration/portfolio-strategies/ABCD',
                         json=strategy).mock(return_value=Response(200))
        await copy_factory_client.update_portfolio_strategy('ABCD', strategy)
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/' \
                                            f'portfolio-strategies/ABCD'
        assert rsps.calls[0].request.method == 'PUT'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert rsps.calls[0].request.content == json.dumps(strategy).encode('utf-8')

    @pytest.mark.asyncio
    async def test_not_update_portfolio_strategy_with_account_token(self):
        """Should not update portfolio strategy via API with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.update_portfolio_strategy('ABCD', {})
        except Exception as err:
            assert err.__str__() == 'You can not invoke update_portfolio_strategy method, because you have connected ' \
                                    'with account access token. Please use API access token from ' \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_remove_portfolio_strategy(self):
        """Should remove portfolio strategy via API."""
        payload = {'mode': 'preserve'}
        rsps = respx.delete(f'{copy_factory_api_url}/users/current/configuration/portfolio-strategies/ABCD')\
            .mock(return_value=Response(204))
        await copy_factory_client.remove_portfolio_strategy('ABCD', payload)
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/' \
                                            f'portfolio-strategies/ABCD'
        assert rsps.calls[0].request.method == 'DELETE'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert rsps.calls[0].request.content == json.dumps(payload).encode('utf-8')

    @pytest.mark.asyncio
    async def test_not_remove_portfolio_strategy_with_account_token(self):
        """Should not remove portfolio strategy with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.remove_portfolio_strategy('ABCD')
        except Exception as err:
            assert err.__str__() == 'You can not invoke remove_portfolio_strategy method, because you have ' \
                                    'connected with account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_copyfactory_subscribers_from_api(self):
        """Should retrieve CopyFactory subscribers from API."""
        expected = [{
          '_id': 'e8867baa-5ec2-45ae-9930-4d5cea18d0d6',
          'name': 'Demo account',
          'reservedMarginFraction': 0.25,
          'subscriptions': [
            {
              'strategyId': 'ABCD',
              'multiplier': 1
            }
          ]
        }]
        rsps = respx.get(f'{copy_factory_api_url}/users/current/configuration/subscribers')\
            .mock(return_value=Response(200, json=expected))
        accounts = await copy_factory_client.get_subscribers()
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/subscribers'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert accounts == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_copyfactory_subscribers_with_account_token(self):
        """Should not retrieve CopyFactory subscribers via API with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.get_subscribers()
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_subscribers method, because you have connected with ' + \
                                    'account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_retrieve_copyfactory_subscriber_from_api(self):
        """Should retrieve CopyFactory subscriber from API."""
        expected = {
            '_id': 'e8867baa-5ec2-45ae-9930-4d5cea18d0d6',
            'name': 'Demo account',
            'reservedMarginFraction': 0.25,
            'subscriptions': [
                {
                    'strategyId': 'ABCD',
                    'multiplier': 1
                }
            ]
        }
        rsps = respx.get(f'{copy_factory_api_url}/users/current/configuration/subscribers/' +
                         'e8867baa-5ec2-45ae-9930-4d5cea18d0d6').mock(return_value=Response(200, json=expected))
        accounts = await copy_factory_client.get_subscriber('e8867baa-5ec2-45ae-9930-4d5cea18d0d6')
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/subscribers/' + \
               'e8867baa-5ec2-45ae-9930-4d5cea18d0d6'
        assert rsps.calls[0].request.method == 'GET'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert accounts == expected

    @pytest.mark.asyncio
    async def test_not_retrieve_copyfactory_subscriber_with_account_token(self):
        """Should not retrieve CopyFactory subscriber from API with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.get_subscriber('test')
        except Exception as err:
            assert err.__str__() == 'You can not invoke get_subscriber method, because you have connected with ' + \
                                    'account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_copyfactory_subscriber(self):
        """Should update CopyFactory subscriber via API."""
        subscriber = {
            'name': 'Demo account',
            'reservedMarginFraction': 0.25,
            'subscriptions': [
                {
                    'strategyId': 'ABCD',
                    'multiplier': 1
                }
            ]
        }
        rsps = respx.put(f'{copy_factory_api_url}/users/current/configuration/subscribers/' +
                         'e8867baa-5ec2-45ae-9930-4d5cea18d0d6', json=subscriber).mock(return_value=Response(200))
        await copy_factory_client.update_subscriber('e8867baa-5ec2-45ae-9930-4d5cea18d0d6', subscriber)
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/subscribers/' + \
                                            'e8867baa-5ec2-45ae-9930-4d5cea18d0d6'
        assert rsps.calls[0].request.method == 'PUT'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'
        assert rsps.calls[0].request.read() == json.dumps(subscriber).encode('utf-8')

    @pytest.mark.asyncio
    async def test_not_update_copyfactory_subscriber_with_account_token(self):
        """Should not update CopyFactory subscriber via API with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.update_subscriber('id', {})
        except Exception as err:
            assert err.__str__() == 'You can not invoke update_subscriber method, because you have connected with ' + \
                                    'account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'

    @respx.mock
    @pytest.mark.asyncio
    async def test_remove_copyfactory_subscriber(self):
        """Should remove CopyFactory subscriber via API."""
        rsps = respx.delete(f'{copy_factory_api_url}/users/current/configuration/subscribers/' +
                            'e8867baa-5ec2-45ae-9930-4d5cea18d0d6').mock(return_value=Response(204))
        await copy_factory_client.remove_subscriber('e8867baa-5ec2-45ae-9930-4d5cea18d0d6')
        assert rsps.calls[0].request.url == f'{copy_factory_api_url}/users/current/configuration/subscribers/' + \
               'e8867baa-5ec2-45ae-9930-4d5cea18d0d6'
        assert rsps.calls[0].request.method == 'DELETE'
        assert rsps.calls[0].request.headers['auth-token'] == 'header.payload.sign'

    @pytest.mark.asyncio
    async def test_not_remove_copyfactory_subscriber_with_account_token(self):
        """Should not remove CopyFactory subscriber via API with account token."""
        copy_factory_client = ConfigurationClient(http_client, 'token')
        try:
            await copy_factory_client.remove_subscriber('id')
        except Exception as err:
            assert err.__str__() == 'You can not invoke remove_subscriber method, because you have connected with ' + \
                                    'account access token. Please use API access token from ' + \
                                    'https://app.metaapi.cloud/token page to invoke this method.'
