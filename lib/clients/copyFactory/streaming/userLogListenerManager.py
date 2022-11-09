from ...metaApi_client import MetaApiClient
from ...domain_client import DomainClient
from ....models import random_id, format_date, date
from ...errorHandler import NotFoundException
from .userLogListener import UserLogListener
from ..copyFactory_models import LogLevel
from datetime import datetime, timedelta
from ....logger import LoggerManager
import asyncio
import math


class UserLogListenerManager(MetaApiClient):
    """User log listener manager."""

    def __init__(self, domain_client: DomainClient):
        """Inits user log listener manager instance.

        Args:
            domain_client: Domain client.
        """
        super().__init__(domain_client)
        self._domainClient = domain_client
        self._strategyLogListeners = {}
        self._subscriberLogListeners = {}
        self._errorThrottleTime = 1
        self._logger = LoggerManager.get_logger('UserLogListenerManager')

    @property
    def strategy_log_listeners(self):
        """Returns the dictionary of strategy log listeners.

        Returns:
            Dictionary of strategy log listeners.
        """
        return self._strategyLogListeners

    @property
    def subscriber_log_listeners(self):
        """Returns the dictionary of subscriber log listeners.

        Returns:
            Dictionary of subscriber log listeners.
        """
        return self._subscriberLogListeners

    def add_strategy_log_listener(self, listener: UserLogListener, strategy_id: str, start_time: datetime = None,
                                  position_id: str = None, level: LogLevel = None, limit: int = None):
        """Adds a strategy transaction listener.

        Args:
            listener: User transaction listener.
            strategy_id: Strategy id.
            start_time: Transaction search start time.
            position_id: Position id filter.
            level: Minimum severity level.
            limit: Log pagination limit.

        Returns:
            Strategy log listener id.
        """
        listener_id = random_id(10)
        self._strategyLogListeners[listener_id] = listener
        asyncio.create_task(self._start_strategy_log_stream_job(listener_id, listener, strategy_id, start_time,
                                                                position_id, level, limit))
        return listener_id

    def add_subscriber_log_listener(self, listener: UserLogListener, subscriber_id: str, start_time: datetime = None,
                                    strategy_id: str = None, position_id: str = None, level: LogLevel = None,
                                    limit: int = None):
        """Adds a subscriber transaction listener.

        Args:
            listener: User transaction listener.
            subscriber_id: Subscriber id.
            start_time: Transaction search start time.
            strategy_id: Strategy id filter.
            position_id: Position id filter.
            level: Minimum severity level.
            limit: Log pagination limit.

        Returns:
            Subscriber transaction listener id.
        """
        listener_id = random_id(10)
        self._subscriberLogListeners[listener_id] = listener
        asyncio.create_task(self._start_subscriber_log_stream_job(listener_id, listener, subscriber_id, start_time,
                                                                  strategy_id, position_id, level, limit))
        return listener_id

    def remove_strategy_log_listener(self, listener_id: str):
        """Removes strategy log listener by id.

        Args:
            listener_id: Listener id.
        """
        if listener_id in self._strategyLogListeners:
            del self._strategyLogListeners[listener_id]

    def remove_subscriber_log_listener(self, listener_id: str):
        """Removes subscriber transaction listener by id.

        Args:
            listener_id: Listener id.
        """
        if listener_id in self._subscriberLogListeners:
            del self._subscriberLogListeners[listener_id]

    async def _start_strategy_log_stream_job(self, listener_id: str, listener: UserLogListener,
                                             strategy_id: str, start_time: datetime = None, position_id: str = None,
                                             level: LogLevel = None, limit: int = None):
        throttle_time = self._errorThrottleTime
        while listener_id in self._strategyLogListeners:
            opts = {
                'url': f'/users/current/strategies/{strategy_id}/user-log/stream',
                'method': 'GET',
                'params': {},
                'headers': {
                    'auth-token': self._token
                }
            }
            if start_time:
                opts['params']['startTime'] = format_date(start_time)
            if position_id:
                opts['params']['positionId'] = position_id
            if level:
                opts['params']['level'] = level
            if limit:
                opts['params']['limit'] = limit
            try:
                packets = await self._domainClient.request_copyfactory(opts, True)
                # stop job if user has unsubscribed in time of new packets has been received
                if listener_id not in self._strategyLogListeners:
                    return
                await listener.on_user_log(packets)
                throttle_time = self._errorThrottleTime
                if listener_id in self._strategyLogListeners and len(packets):
                    start_time = date(packets[0]['time']) + timedelta(milliseconds=1)
            except NotFoundException as err:
                await listener.on_error(err)
                self._logger.error(f'Strategy {strategy_id} not found, removing listener f{listener_id}')
                if listener_id in self._strategyLogListeners:
                    del self._strategyLogListeners[listener_id]
            except Exception as err:
                await listener.on_error(err)
                self._logger.error(f'Failed to retrieve user log stream for strategy {strategy_id}, ' +
                                   f'listener {listener_id}, retrying in {math.floor(throttle_time)} seconds', err)
                await asyncio.sleep(throttle_time)
                throttle_time = min(throttle_time * 2, 30)

    async def _start_subscriber_log_stream_job(self, listener_id: str, listener: UserLogListener, subscriber_id: str,
                                               start_time: datetime = None, strategy_id: str = None,
                                               position_id: str = None, level: LogLevel = None, limit: int = None):
        throttle_time = self._errorThrottleTime
        while listener_id in self._subscriberLogListeners:
            opts = {
                'url': f'/users/current/subscribers/{subscriber_id}/user-log/stream',
                'method': 'GET',
                'params': {},
                'headers': {
                    'auth-token': self._token
                }
            }
            if start_time:
                opts['params']['startTime'] = format_date(start_time)
            if strategy_id:
                opts['params']['strategyId'] = strategy_id
            if position_id:
                opts['params']['positionId'] = position_id
            if level:
                opts['params']['level'] = level
            if limit:
                opts['params']['limit'] = limit
            try:
                packets = await self._domainClient.request_copyfactory(opts, True)
                # stop job if user has unsubscribed in time of new packets has been received
                if listener_id not in self._subscriberLogListeners:
                    return
                await listener.on_user_log(packets)
                throttle_time = self._errorThrottleTime
                if listener_id in self._subscriberLogListeners and len(packets):
                    start_time = date(packets[0]['time']) + timedelta(milliseconds=1)
            except NotFoundException as err:
                await listener.on_error(err)
                self._logger.error(f'Subscriber {subscriber_id} not found, removing listener f{listener_id}')
                if listener_id in self._subscriberLogListeners:
                    del self._subscriberLogListeners[listener_id]
            except Exception as err:
                await listener.on_error(err)
                self._logger.error(f'Failed to retrieve user log stream for subscriber {subscriber_id}, ' +
                                   f'listener {listener_id}, retrying in {math.floor(throttle_time)} seconds', err)
                await asyncio.sleep(throttle_time)
                throttle_time = min(throttle_time * 2, 30)
