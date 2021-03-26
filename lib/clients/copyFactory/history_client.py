from ..metaApi_client import MetaApiClient
from ...models import date, format_date
from .copyFactory_models import CopyFactoryTransaction, CopyFactoryStrategyIdAndName, CopyFactorySubscriberOrProvider
from datetime import datetime
from typing import List
from httpx import Response


class HistoryClient(MetaApiClient):
    """metaapi.cloud CopyFactory history API (trade copying history API) client (see
    https://metaapi.cloud/docs/copyfactory/)"""

    def __init__(self, http_client, token: str, domain: str = 'agiliumtrade.agiliumtrade.ai'):
        """Inits CopyFactory history API client instance.

        Args:
            http_client: HTTP client.
            token: Authorization token.
            domain: Domain to connect to, default is agiliumtrade.agiliumtrade.ai.
        """
        super().__init__(http_client, token, domain)
        self._host = f'https://trading-api-v1.{domain}'

    async def get_providers(self) -> 'Response[List[CopyFactorySubscriberOrProvider]]':
        """Returns list of providers providing strategies to the current user
        https://metaapi.cloud/docs/copyfactory/restApi/api/history/getProviders/

        Returns:
            A coroutine resolving with providers found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_providers')
        opts = {
            'url': f"{self._host}/users/current/providers",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_subscribers(self) -> 'Response[List[CopyFactorySubscriberOrProvider]]':
        """Returns list of subscribers providing strategies to the current user
        https://metaapi.cloud/docs/copyfactory/restApi/api/history/getSubscribers/

        Returns:
            A coroutine resolving with subscribers found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_subscribers')
        opts = {
            'url': f"{self._host}/users/current/subscribers",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_strategies_subscribed(self) -> 'Response[List[CopyFactoryStrategyIdAndName]]':
        """Returns list of strategies the current user is subscribed to
        https://metaapi.cloud/docs/copyfactory/restApi/api/history/getStrategiesSubscribed/

        Returns:
            A coroutine resolving with strategies found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_strategies_subscribed')
        opts = {
            'url': f"{self._host}/users/current/strategies-subscribed",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_provided_strategies(self) -> 'Response[List[CopyFactoryStrategyIdAndName]]':
        """Returns list of strategies the current user provides to other users
        https://metaapi.cloud/docs/copyfactory/restApi/api/history/getProvidedStrategies/

        Returns:
            A coroutine resolving with strategies found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_provided_strategies')
        opts = {
            'url': f"{self._host}/users/current/provided-strategies",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_provided_strategies_transactions(self, time_from: datetime, time_till: datetime,
                                                   strategy_ids: List[str] = None, subscriber_ids: List[str] = None,
                                                   offset: int = None, limit: int = None) -> \
            'Response[List[CopyFactoryTransaction]]':
        """Returns list of transactions on the strategies the current user provides to other users
        https://metaapi.cloud/docs/copyfactory/restApi/api/history/getProvidedStrategiesTransactions/

        Args:
            time_from: Time to load transactions from.
            time_till: Time to load transactions till.
            strategy_ids: Optional list of strategy ids to filter transactions by.
            subscriber_ids: Optional list of subscribers to filter transactions by.
            offset: Pagination offset. Default value is 0.
            limit: Pagination limit. Default value is 1000.

        Returns:
            A coroutine resolving with transactions found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_provided_strategies_transactions')
        qs = {
            'from': format_date(time_from),
            'till': format_date(time_till)
        }
        if strategy_ids:
            qs['strategyId'] = strategy_ids
        if subscriber_ids:
            qs['subscriberId'] = subscriber_ids
        if not (offset is None):
            qs['offset'] = offset
        if limit:
            qs['limit'] = limit
        opts = {
          'url': f'{self._host}/users/current/provided-strategies/transactions',
          'method': 'GET',
          'headers': {
            'auth-token': self._token
          },
          'params': qs
        }
        transactions = await self._httpClient.request(opts)
        for transaction in transactions:
            transaction['time'] = date(transaction['time'])
        return transactions

    async def get_strategies_subscribed_transactions(self, time_from: datetime, time_till: datetime,
                                                     strategy_ids: List[str] = None, provider_ids: List[str] = None,
                                                     offset: int = None, limit: int = None) -> \
            'Response[List[CopyFactoryTransaction]]':
        """Returns list of trades on the strategies the current user subscribed to
        https://metaapi.cloud/docs/copyfactory/restApi/api/history/getStrategiesSubscribedTransactions/

        Args:
            time_from: Time to load transactions from.
            time_till: Time to load transactions till.
            strategy_ids: Optional list of strategy ids to filter transactions by.
            provider_ids: Optional list of providers to filter transactions by.
            offset: Pagination offset. Default value is 0.
            limit: Pagination limit. Default value is 1000.

        Returns:
            A coroutine resolving with transactions found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_strategies_subscribed_transactions')
        qs = {
            'from': format_date(time_from),
            'till': format_date(time_till)
        }
        if strategy_ids:
            qs['strategyId'] = strategy_ids
        if provider_ids:
            qs['providerId'] = provider_ids
        if not (offset is None):
            qs['offset'] = offset
        if limit:
            qs['limit'] = limit
        opts = {
          'url': f'{self._host}/users/current/strategies-subscribed/transactions',
          'method': 'GET',
          'headers': {
            'auth-token': self._token
          },
          'params': qs
        }
        transactions = await self._httpClient.request(opts)
        for transaction in transactions:
            transaction['time'] = date(transaction['time'])
        return transactions
