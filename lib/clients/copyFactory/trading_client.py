from ..metaApi_client import MetaApiClient
from ..domain_client import DomainClient
from .streaming.stopoutListenerManager import StopoutListenerManager
from .streaming.userLogListenerManager import UserLogListenerManager
from .signal_client import SignalClient
from .copyFactory_models import CopyFactoryStrategyStopout, CopyFactoryUserLogMessage, \
    CopyFactoryStrategyStopoutReason, LogLevel
from .streaming.stopoutListener import StopoutListener
from .streaming.userLogListener import UserLogListener
from typing import List
from httpx import Response
from datetime import datetime
from ...models import format_date, convert_iso_time_to_date


class TradingClient(MetaApiClient):
    """metaapi.cloud CopyFactory trading API (trade copying trading API) client (see
    https://metaapi.cloud/docs/copyfactory/)"""

    def __init__(self, domain_client: DomainClient):
        """Inits CopyFactory trading API client instance.

        Args:
            domain_client: Domain client.
        """
        super().__init__(domain_client)
        self._domainClient = domain_client
        self._stopoutListenerManager = StopoutListenerManager(domain_client)
        self._userLogListenerManager = UserLogListenerManager(domain_client)

    async def resynchronize(self, subscriber_id: str, strategy_ids: List[str] = None,
                            position_ids: List[str] = None) -> Response:
        """Resynchronizes the account. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/resynchronize/

        Args:
            subscriber_id: Account id.
            strategy_ids: Array of strategy ids to resynchronize. Default is to synchronize all strategies.
            position_ids: Array of position ids to resynchronize. Default is to synchronize all positions.

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
          'url': f'/users/current/subscribers/{subscriber_id}/resynchronize',
          'method': 'POST',
          'headers': {
            'auth-token': self._token
          },
          'params': qs,
        }
        return await self._domainClient.request_copyfactory(opts)

    async def get_signal_client(self, account_id: str):
        """Generates an instance of signal client for an account.

        Args:
            account_id: Account id.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_signal_client')

        account_data = await self._domainClient.get_account_info(account_id)
        host = await self._domainClient.get_signal_client_host(account_data['regions'])
        return SignalClient(account_data['id'], host, self._domainClient)

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
            'url': f'/users/current/subscribers/{subscriber_id}/stopouts',
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        result = await self._domainClient.request_copyfactory(opts)
        convert_iso_time_to_date(result)
        return result

    async def reset_stopouts(self, subscriber_id: str, strategy_id: str, reason: CopyFactoryStrategyStopoutReason) \
            -> Response:
        """Resets strategy stopouts. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/resetStopOuts/

        Args:
            subscriber_id: Account id.
            strategy_id: Strategy id.
            reason: Stopout reason to reset.

        Returns:
            A coroutine which resolves when the stopouts are reset.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('reset_stopouts')
        opts = {
            'url': f'/users/current/subscribers/{subscriber_id}/subscription-strategies/{strategy_id}' +
                   f'/stopouts/{reason}/reset',
            'method': 'POST',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._domainClient.request_copyfactory(opts)

    async def get_user_log(self, subscriber_id: str, start_time: datetime = None, end_time: datetime = None,
                           strategy_id: str = None, position_id: str = None, level: LogLevel = None,
                           offset: int = 0, limit: int = 1000) -> 'List[CopyFactoryUserLogMessage]':
        """Returns copy trading user log for an account and time range, sorted in reverse chronological order. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/getUserLog/

        Args:
            subscriber_id: Subscriber id.
            start_time: Time to start loading data from.
            end_time: Time to stop loading data at.
            strategy_id: Strategy id filter.
            position_id: Position id filter.
            level: Minimum severity level.
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
        if strategy_id:
            qs['strategyId'] = strategy_id
        if position_id:
            qs['positionId'] = position_id
        if level:
            qs['level'] = level
        opts = {
            'url': f'/users/current/subscribers/{subscriber_id}/user-log',
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            },
            'params': qs
        }
        result = await self._domainClient.request_copyfactory(opts, True)
        convert_iso_time_to_date(result)
        return result

    async def get_strategy_log(self, strategy_id: str, start_time: datetime = None, end_time: datetime = None,
                               position_id: str = None, level: LogLevel = None,
                               offset: int = 0, limit: int = 1000) -> 'List[CopyFactoryUserLogMessage]':
        """Returns event log for CopyFactory strategy, sorted in reverse chronological order. See
        https://metaapi.cloud/docs/copyfactory/restApi/api/trading/getStrategyLog/

        Args:
            strategy_id: Strategy id to retrieve log for.
            start_time: Time to start loading data from.
            end_time: Time to stop loading data at.
            position_id: Position id filter.
            level: Minimum severity level.
            offset: Pagination offset. Default is 0.
            limit: Pagination limit. Default is 1000.

        Returns:
            A coroutine which resolves with log records found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_strategy_log')
        qs = {
            'offset': offset,
            'limit': limit
        }
        if start_time:
            qs['startTime'] = format_date(start_time)
        if end_time:
            qs['endTime'] = format_date(end_time)
        if position_id:
            qs['positionId'] = position_id
        if level:
            qs['level'] = level
        opts = {
            'url': f'/users/current/strategies/{strategy_id}/user-log',
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            },
            'params': qs
        }
        result = await self._domainClient.request_copyfactory(opts, True)
        convert_iso_time_to_date(result)
        return result

    def add_stopout_listener(self, listener: StopoutListener, account_id: str = None, strategy_id: str = None,
                             sequence_number: int = None) -> str:
        """Adds a stopout listener and creates a job to make requests.

        Args:
            listener: Stopout listener.
            account_id: Account id.
            strategy_id: Strategy id.
            sequence_number: Sequence number.

        Returns:
            Listener id.
        """
        return self._stopoutListenerManager.add_stopout_listener(listener, account_id, strategy_id, sequence_number)

    def remove_stopout_listener(self, listener_id: str):
        """Removes stopout listener and cancels the event stream.

        Args:
            listener_id: Stopout listener id.
        """
        self._stopoutListenerManager.remove_stopout_listener(listener_id)

    def add_strategy_log_listener(self, listener: UserLogListener, strategy_id: str, start_time: datetime = None,
                                  position_id: str = None, level: LogLevel = None, limit: int = None) -> str:
        """Adds a strategy log listener and creates a job to make requests.

        Args:
            listener: User log listener.
            strategy_id: Strategy id.
            start_time: Log search start time.
            position_id: Position id filter.
            level: Minimum severity level.
            limit: Log pagination limit.

        Returns:
            Listener id.
        """
        return self._userLogListenerManager.add_strategy_log_listener(listener, strategy_id, start_time, position_id,
                                                                      level, limit)

    def remove_strategy_log_listener(self, listener_id: str):
        """Removes strategy log listener and cancels the event stream.

        Args:
            listener_id: Strategy log listener id.
        """
        self._userLogListenerManager.remove_strategy_log_listener(listener_id)

    def add_subscriber_log_listener(self, listener: UserLogListener, subscriber_id: str, start_time: datetime = None,
                                    strategy_id: str = None, position_id: str = None, level: LogLevel = None,
                                    limit: int = None) -> str:
        """Adds a subscriber log listener and creates a job to make requests.

        Args:
            listener: User log listener.
            subscriber_id: Subscriber id.
            start_time: Log search start time.
            strategy_id: Strategy id filter.
            position_id: Position id filter.
            level: Minimum severity level.
            limit: Log pagination limit.

        Returns:
            Listener id.
        """
        return self._userLogListenerManager.add_subscriber_log_listener(
            listener, subscriber_id, start_time, strategy_id, position_id, level, limit)

    def remove_subscriber_log_listener(self, listener_id: str):
        """Removes subscriber log listener and cancels the event stream.

        Args:
            listener_id: Subscriber log listener id.
        """
        self._userLogListenerManager.remove_subscriber_log_listener(listener_id)
