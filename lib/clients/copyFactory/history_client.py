from ..metaApi_client import MetaApiClient
from ...models import format_date, convert_iso_time_to_date
from .copyFactory_models import CopyFactoryTransaction
from datetime import datetime
from typing import List


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
        self._host = f'https://copyfactory-application-history-master-v1.{domain}'

    async def get_provided_strategies_transactions(self, time_from: datetime, time_till: datetime,
                                                   strategy_ids: List[str] = None, account_ids: List[str] = None,
                                                   offset: int = None, limit: int = None) -> \
            'List[CopyFactoryTransaction]':
        """Returns list of transactions on the strategies the current user provides to other users. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/history/getProvidedStrategiesTransactions/

        Args:
            time_from: Time to load transactions from.
            time_till: Time to load transactions till.
            strategy_ids: Optional list of strategy ids to filter transactions by.
            account_ids: The list of CopyFactory subscriber account id (64-character long) to filter by.
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
        if account_ids:
            qs['accountId'] = account_ids
        if not (offset is None):
            qs['offset'] = offset
        if limit:
            qs['limit'] = limit
        opts = {
          'url': f'{self._host}/users/current/provided-transactions',
          'method': 'GET',
          'headers': {
            'auth-token': self._token
          },
          'params': qs
        }
        transactions = await self._httpClient.request(opts)
        convert_iso_time_to_date(transactions)
        return transactions

    async def get_strategies_subscribed_transactions(self, time_from: datetime, time_till: datetime,
                                                     strategy_ids: List[str] = None, account_ids: List[str] = None,
                                                     offset: int = None, limit: int = None) -> \
            'List[CopyFactoryTransaction]':
        """Returns list of trades on the strategies the current user subscribed to
        https://metaapi.cloud/docs/copyfactory/restApi/api/history/getStrategiesSubscribedTransactions/

        Args:
            time_from: Time to load transactions from.
            time_till: Time to load transactions till.
            strategy_ids: Optional list of strategy ids to filter transactions by.
            account_ids: The list of CopyFactory subscriber account id (64-character long) to filter by.
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
        if account_ids:
            qs['accountId'] = account_ids
        if not (offset is None):
            qs['offset'] = offset
        if limit:
            qs['limit'] = limit
        opts = {
          'url': f'{self._host}/users/current/subscription-transactions',
          'method': 'GET',
          'headers': {
            'auth-token': self._token
          },
          'params': qs
        }
        transactions = await self._httpClient.request(opts)
        convert_iso_time_to_date(transactions)
        return transactions
