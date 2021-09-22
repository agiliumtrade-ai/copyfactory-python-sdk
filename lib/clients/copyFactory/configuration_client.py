from ..metaApi_client import MetaApiClient
from ...models import random_id, convert_iso_time_to_date, format_request
from .copyFactory_models import StrategyId, CopyFactoryStrategyUpdate, CopyFactorySubscriberUpdate, \
    CopyFactorySubscriber, CopyFactoryStrategy, CopyFactoryPortfolioStrategy, \
    CopyFactoryPortfolioStrategyUpdate, CopyFactoryCloseInstructions
from typing import List
from copy import deepcopy


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
        self._host = f'https://copyfactory-application-history-master-v1.{domain}'

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

    @staticmethod
    def generate_account_id() -> str:
        """Generates random account id.

        Returns:
            Account id.
        """
        return random_id(64)

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
        result = await self._httpClient.request(opts)
        convert_iso_time_to_date(result)
        return result

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
        strategy = await self._httpClient.request(opts)
        convert_iso_time_to_date(strategy)
        return strategy

    async def update_strategy(self, strategy_id: str, strategy: CopyFactoryStrategyUpdate):
        """Updates a CopyFactory strategy. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/updateStrategy/

        Args:
            strategy_id: Copy trading strategy id.
            strategy: Trading strategy update.

        Returns:
            A coroutine resolving when strategy is updated.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('update_strategy')
        payload = deepcopy(strategy)
        format_request(payload)
        opts = {
            'url': f"{self._host}/users/current/configuration/strategies/{strategy_id}",
            'method': 'PUT',
            'headers': {
                'auth-token': self._token
            },
            'body': payload
        }
        return await self._httpClient.request(opts)

    async def remove_strategy(self, strategy_id: str, close_instructions: CopyFactoryCloseInstructions = None):
        """Deletes a CopyFactory strategy. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/removeStrategy/

        Args:
            strategy_id: Copy trading strategy id.
            close_instructions: Strategy close instructions.

        Returns:
            A coroutine resolving when strategy is removed.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('remove_strategy')
        opts = {
            'url': f"{self._host}/users/current/configuration/strategies/{strategy_id}",
            'method': 'DELETE',
            'headers': {
                'auth-token': self._token
            }
        }
        if close_instructions is not None:
            opts['body'] = close_instructions
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
        result = await self._httpClient.request(opts)
        convert_iso_time_to_date(result)
        return result

    async def get_portfolio_strategy(self, portfolio_id: str) -> CopyFactoryPortfolioStrategy:
        """Retrieves a CopyFactory copy portfolio strategy by id. See
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
        strategy = await self._httpClient.request(opts)
        convert_iso_time_to_date(strategy)
        return strategy

    async def update_portfolio_strategy(self, portfolio_id: str, portfolio: CopyFactoryPortfolioStrategyUpdate):
        """Updates a CopyFactory portfolio strategy. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/updatePortfolioStrategy/

        Args:
            portfolio_id: Copy trading portfolio strategy id.
            portfolio: Portfolio strategy update.

        Returns:
            A coroutine resolving when portfolio strategy is updated.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('update_portfolio_strategy')
        payload = deepcopy(portfolio)
        format_request(payload)
        opts = {
            'url': f"{self._host}/users/current/configuration/portfolio-strategies/{portfolio_id}",
            'method': 'PUT',
            'headers': {
                'auth-token': self._token
            },
            'body': payload
        }
        return await self._httpClient.request(opts)

    async def remove_portfolio_strategy(self, portfolio_id: str,
                                        close_instructions: CopyFactoryCloseInstructions = None):
        """Deletes a CopyFactory portfolio strategy. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/removePortfolioStrategy/

        Args:
            portfolio_id: Portfolio strategy id.
            close_instructions: Portfolio close instructions.

        Returns:
            A coroutine resolving when portfolio strategy is removed.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('remove_portfolio_strategy')
        opts = {
            'url': f"{self._host}/users/current/configuration/portfolio-strategies/{portfolio_id}",
            'method': 'DELETE',
            'headers': {
                'auth-token': self._token
            }
        }
        if close_instructions is not None:
            opts['body'] = close_instructions
        return await self._httpClient.request(opts)

    async def get_subscribers(self) -> 'List[CopyFactorySubscriber]':
        """Returns CopyFactory subscribers the user has configured. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/getSubscribers/

        Returns:
            A coroutine resolving with subscribers found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_subscribers')
        opts = {
            'url': f"{self._host}/users/current/configuration/subscribers",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        result = await self._httpClient.request(opts)
        convert_iso_time_to_date(result)
        return result

    async def get_subscriber(self, subscriber_id: str) -> CopyFactorySubscriber:
        """Returns CopyFactory subscriber by id. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/getSubscriber/

        Args:
            subscriber_id: Subscriber id.

        Returns:
            A coroutine resolving with subscriber configuration found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_subscriber')
        opts = {
            'url': f"{self._host}/users/current/configuration/subscribers/{subscriber_id}",
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        subscriber = await self._httpClient.request(opts)
        convert_iso_time_to_date(subscriber)
        return subscriber

    async def update_subscriber(self, subscriber_id: str, subscriber: CopyFactorySubscriberUpdate):
        """Updates CopyFactory subscriber configuration. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/updateSubscriber/

        Args:
            subscriber_id: Subscriber id.
            subscriber: Subscriber update.

        Returns:
            A coroutine resolving when subscriber configuration is updated.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('update_subscriber')
        payload = deepcopy(subscriber)
        format_request(payload)
        opts = {
            'url': f"{self._host}/users/current/configuration/subscribers/{subscriber_id}",
            'method': 'PUT',
            'headers': {
                'auth-token': self._token
            },
            'body': payload
        }
        return await self._httpClient.request(opts)

    async def remove_subscriber(self, subscriber_id: str):
        """Deletes subscriber configuration. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/configuration/removeSubscriber/

        Args:
            subscriber_id: Subscriber id.

        Returns:
            A coroutine resolving when subscriber configuration is removed.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('remove_subscriber')
        opts = {
            'url': f"{self._host}/users/current/configuration/subscribers/{subscriber_id}",
            'method': 'DELETE',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)
