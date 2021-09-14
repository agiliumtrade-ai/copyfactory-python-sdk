from ..metaApi_client import MetaApiClient
from .copyFactory_models import CopyFactoryStrategyStopout, CopyFactoryUserLogMessage, \
    CopyFactoryExternalSignalUpdate, CopyFactoryExternalSignalRemove, CopyFactoryTradingSignal
from typing import List
from httpx import Response
from datetime import datetime
from copy import deepcopy
from ...models import format_date, convert_iso_time_to_date, format_request, random_id


class TradingClient(MetaApiClient):
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

    @staticmethod
    def generate_signal_id():
        """Generates random signal id.

        Returns:
            Signal id.
        """
        return random_id(8)

    async def update_external_signal(self, strategy_id: str, signal_id: str, signal: CopyFactoryExternalSignalUpdate):
        """Updates external signal for a strategy. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/updateExternalSignal/

        Args:
            strategy_id: Strategy id.
            signal_id: External signal id (should be 8 alphanumerical symbols)
            signal: Signal update payload.

        Returns:
            A coroutine which resolves when external signal is updated.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('update_external_signal')
        payload: dict = deepcopy(signal)
        format_request(payload)
        opts = {
            'url': f"{self._host}/users/current/strategies/{strategy_id}/external-signals/{signal_id}",
            'method': 'PUT',
            'headers': {
                'auth-token': self._token
            },
            'body': payload
        }
        return await self._httpClient.request(opts)

    async def remove_external_signal(self, strategy_id: str, signal_id: str, signal: CopyFactoryExternalSignalRemove):
        """Removes (closes) external signal for a strategy. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/removeExternalSignal/

        Args:
            strategy_id: Strategy id.
            signal_id: External signal id
            signal: Signal removal payload.

        Returns:
            A coroutine which resolves when external signal is removed.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('remove_external_signal')
        payload: dict = deepcopy(signal)
        format_request(payload)
        opts = {
            'url': f"{self._host}/users/current/strategies/{strategy_id}/external-signals/{signal_id}/remove",
            'method': 'POST',
            'headers': {
                'auth-token': self._token
            },
            'body': payload
        }
        return await self._httpClient.request(opts)

    async def resynchronize(self, subscriber_id: str, strategy_ids: List[str] = None,
                            position_ids: List[str] = None) -> Response:
        """Resynchronizes the account. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/resynchronize/

        Args:
            subscriber_id: Account id.
            strategy_ids: Optional array of strategy ids to resynchronize. Default is to synchronize all strategies.
            position_ids: Optional array of position ids to resynchronize. Default is to synchronize all positions.

        Returns:
            A coroutine which resolves when resynchronization is scheduled.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('resynchronize')
        qs = {}
        if strategy_ids:
            qs['strategyId'] = strategy_ids
        if position_ids:
            qs['positionId'] = position_ids
        opts = {
          'url': f'{self._host}/users/current/subscribers/{subscriber_id}/resynchronize',
          'method': 'POST',
          'headers': {
            'auth-token': self._token
          },
          'params': qs,
        }
        return await self._httpClient.request(opts)

    async def get_trading_signals(self, subscriber_id: str) -> 'List[CopyFactoryTradingSignal]':
        """Returns trading signals the subscriber is subscribed to. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/getTradingSignals/

        Args:
            subscriber_id: Subscriber id.

        Returns:
            A coroutine which resolves with signals found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_signals')
        opts = {
            'url': f'{self._host}/users/current/subscribers/{subscriber_id}/signals',
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        result = await self._httpClient.request(opts)
        convert_iso_time_to_date(result)
        return result

    async def get_stopouts(self, subscriber_id: str) -> 'List[CopyFactoryStrategyStopout]':
        """Returns subscriber account stopouts. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/getStopOuts/

        Args:
            subscriber_id: Account id.

        Returns:
            A coroutine which resolves with stopouts found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_stopouts')
        opts = {
            'url': f'{self._host}/users/current/subscribers/{subscriber_id}/stopouts',
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        result = await self._httpClient.request(opts)
        convert_iso_time_to_date(result)
        return result

    async def reset_stopouts(self, subscriber_id: str, strategy_id: str, reason: str) -> Response:
        """Resets strategy stopouts. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/resetStopOuts/

        Args:
            subscriber_id: Account id.
            strategy_id: Strategy id.
            reason: Stopout reason to reset. One of yearly-balance, monthly-balance, daily-balance, yearly-equity,
            monthly-equity, daily-equity, max-drawdown.

        Returns:
            A coroutine which resolves when the stopouts are reset.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('reset_stopouts')
        opts = {
            'url': f'{self._host}/users/current/subscribers/{subscriber_id}/subscription-strategies/{strategy_id}' +
                   f'/stopouts/{reason}/reset',
            'method': 'POST',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_user_log(self, subscriber_id: str, start_time: datetime = None, end_time: datetime = None,
                           offset: int = 0, limit: int = 1000) -> 'List[CopyFactoryUserLogMessage]':
        """Returns copy trading user log for an account and time range, sorted in reverse chronological order. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/getUserLog/

        Args:
            subscriber_id: Subscriber id.
            start_time: Time to start loading data from.
            end_time: Time to stop loading data at.
            offset: Pagination offset. Default is 0.
            limit: Pagination limit. Default is 1000.

        Returns:
            A coroutine which resolves with log records found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_user_log')
        qs = {
            'offset': offset,
            'limit': limit
        }
        if start_time:
            qs['startTime'] = format_date(start_time)
        if end_time:
            qs['endTime'] = format_date(end_time)
        opts = {
            'url': f'{self._host}/users/current/subscribers/{subscriber_id}/user-log',
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            },
            'params': qs
        }
        result = await self._httpClient.request(opts)
        convert_iso_time_to_date(result)
        return result
