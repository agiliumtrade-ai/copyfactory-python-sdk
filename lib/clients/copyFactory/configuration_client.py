from ..metaApi_client import MetaApiClient
from ...models import random_id, date
from .copyFactory_models import StrategyId, CopyFactoryAccountUpdate, CopyFactoryStrategyUpdate, \
    ResynchronizationTask, CopyFactoryAccount, CopyFactoryStrategy, CopyFactoryPortfolioStrategy, \
    CopyFactoryPortfolioStrategyUpdate
from ..timeoutException import TimeoutException
from datetime import datetime
import asyncio
from typing import List


class ConfigurationClient(MetaApiClient):
    """metaapi.cloud CopyFactory configuration API (trade copying configuration API) client (see
    https://metaapi.cloud/docs/copyfactory/)"""

    def __init__(self, http_client, token: str, domain: str = 'agiliumtrade.agiliumtrade.ai'):
        """Inits CopyFactory configuration API client instance.

        Args:
            http_client: HTTP client.
            token: Authorization token.
            domain: Domain to connect to, default is agiliumtrade.agiliumtrade.ai.
        """
        super().__init__(http_client, token, domain)
        self._host = f'https://trading-api-v1.{domain}'

    async def generate_strategy_id(self) -> StrategyId:
        """Retrieves new unused strategy id. Method is accessible only with API access token. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/generateStrategyId/

        Returns:
            A coroutine resolving with strategy id generated.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('generate_strategy_id')
        opts = {
            'url': f"{self._host}/users/current/configuration/unused-strategy-id",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    def generate_account_id(self) -> str:
        """Generates random account id.

        Returns:
            Account id.
        """
        return random_id(64)

    async def get_accounts(self) -> 'List[CopyFactoryAccount]':
        """Retrieves CopyFactory copy trading accounts. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/getAccounts/

        Returns:
            A coroutine resolving with CopyFactory accounts found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_accounts')
        opts = {
            'url': f"{self._host}/users/current/configuration/accounts",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_account(self, account_id: str) -> CopyFactoryAccount:
        """Retrieves CopyFactory copy trading account by id. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/getAccount/

        Args:
            account_id: CopyFactory account id.

        Returns:
            A coroutine resolving with CopyFactory account found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_account')
        opts = {
            'url': f"{self._host}/users/current/configuration/accounts/{account_id}",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def update_account(self, id: str, account: CopyFactoryAccountUpdate):
        """Updates a CopyFactory trade copying account. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/updateAccount/

        Args:
            id: Copy trading account id.
            account: Trading account update.

        Returns:
            A coroutine resolving when account is updated.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('update_account')
        opts = {
            'url': f"{self._host}/users/current/configuration/accounts/{id}",
            'method': 'PUT',
            'headers': {
                'auth-token': self._token
            },
            'body': account
        }
        return await self._httpClient.request(opts)

    async def remove_account(self, id: str):
        """Removes a CopyFactory trade copying account. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/removeAccount/

        Args:
            id: Copy trading account id.

        Returns:
            A coroutine resolving when account is removed.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('remove_account')
        opts = {
            'url': f"{self._host}/users/current/configuration/accounts/{id}",
            'method': 'DELETE',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_strategies(self) -> 'List[CopyFactoryStrategy]':
        """Retrieves CopyFactory copy trading strategies. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/getStrategies/

        Returns:
            A coroutine resolving with CopyFactory strategies found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_strategies')
        opts = {
            'url': f"{self._host}/users/current/configuration/strategies",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_strategy(self, strategy_id: str) -> CopyFactoryStrategy:
        """Retrieves CopyFactory copy trading strategy by id. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/getStrategy/

        Args:
            strategy_id: Trading strategy id.

        Returns:
            A coroutine resolving with CopyFactory strategy found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_strategy')
        opts = {
            'url': f"{self._host}/users/current/configuration/strategies/{strategy_id}",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def update_strategy(self, id: str, strategy: CopyFactoryStrategyUpdate):
        """Updates a CopyFactory strategy. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/updateStrategy/

        Args:
            id: Copy trading strategy id.
            strategy: Trading strategy update.

        Returns:
            A coroutine resolving when strategy is updated.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('update_strategy')
        opts = {
            'url': f"{self._host}/users/current/configuration/strategies/{id}",
            'method': 'PUT',
            'headers': {
                'auth-token': self._token
            },
            'body': strategy
        }
        return await self._httpClient.request(opts)

    async def remove_strategy(self, id: str):
        """Removes a CopyFactory strategy. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/removeStrategy/

        Args:
            id: Copy trading strategy id.

        Returns:
            A coroutine resolving when strategy is removed.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('remove_strategy')
        opts = {
            'url': f"{self._host}/users/current/configuration/strategies/{id}",
            'method': 'DELETE',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_portfolio_strategies(self) -> 'List[CopyFactoryPortfolioStrategy]':
        """Retrieves CopyFactory copy portfolio strategies. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/getPortfolioStrategies/

        Returns:
            A coroutine resolving with CopyFactory portfolio strategies found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_portfolio_strategies')
        opts = {
            'url': f"{self._host}/users/current/configuration/portfolio-strategies",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_portfolio_strategy(self, portfolio_id: str) -> CopyFactoryPortfolioStrategy:
        """Retrieves CopyFactory copy portfolio strategies. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/getPortfolioStrategy/

        Args:
            portfolio_id: Portfolio strategy id.

        Returns:
            A coroutine resolving with CopyFactory portfolio strategy found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_portfolio_strategy')
        opts = {
            'url': f"{self._host}/users/current/configuration/portfolio-strategies/{portfolio_id}",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def update_portfolio_strategy(self, id: str, strategy: CopyFactoryPortfolioStrategyUpdate):
        """Updates a CopyFactory portfolio strategy. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/updatePortfolioStrategy/

        Args:
            id: Copy trading portfolio strategy id.
            strategy: Portfolio strategy update.

        Returns:
            A coroutine resolving when portfolio strategy is updated.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('update_portfolio_strategy')
        opts = {
            'url': f"{self._host}/users/current/configuration/portfolio-strategies/{id}",
            'method': 'PUT',
            'headers': {
                'auth-token': self._token
            },
            'body': strategy
        }
        return await self._httpClient.request(opts)

    async def remove_portfolio_strategy(self, id: str):
        """Deletes a CopyFactory portfolio strategy. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/removePortfolioStrategy/

        Args:
            id: Portfolio strategy id.

        Returns:
            A coroutine resolving when portfolio strategy is removed.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('remove_portfolio_strategy')
        opts = {
            'url': f"{self._host}/users/current/configuration/portfolio-strategies/{id}",
            'method': 'DELETE',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_active_resynchronization_tasks(self, connection_id) -> 'List[ResynchronizationTask]':
        """Returns list of active resynchronization tasks for a specified connection. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/getActiveResynchronizationTasks/

        Args:
            connection_id: MetaApi account id to return tasks for.

        Returns:
            A coroutine resolving with list of active resynchronization tasks.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_active_resynchronization_tasks')
        opts = {
            'url': f"{self._host}/users/current/configuration/connections/{connection_id}" +
                   "/active-resynchronization-tasks",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }

        tasks = await self._httpClient.request(opts)
        for task in tasks:
            task['createdAt'] = date(task['createdAt'])
        return tasks

    async def wait_resynchronization_tasks_completed(self, connection_id: str, timeout_in_seconds: float = 300,
                                                     interval_in_milliseconds: float = 1000):
        """Waits until active resynchronization tasks are completed.

        Args:
            connection_id: MetaApi account id to wait tasks completed for.
            timeout_in_seconds: Wait timeout in seconds, default is 5m.
            interval_in_milliseconds: Interval between tasks reload while waiting for a change, default is 1s.

        Returns:
            A couroutine which resolves when tasks are completed.

        Raises:
            TimeoutException: If tasks have not completed within timeout allowed.
        """
        start_time = datetime.now().timestamp()
        tasks = await self.get_active_resynchronization_tasks(connection_id)
        while len(tasks) and (start_time + timeout_in_seconds) > datetime.now().timestamp():
            await asyncio.sleep(interval_in_milliseconds / 1000)
            tasks = await self.get_active_resynchronization_tasks(connection_id)
        if len(tasks):
            raise TimeoutException('Timed out waiting for resynchronization tasks for account '
                                   + connection_id + ' to be completed')
