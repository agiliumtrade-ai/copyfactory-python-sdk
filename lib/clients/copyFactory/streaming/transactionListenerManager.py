from ...metaApi_client import MetaApiClient
from ...domain_client import DomainClient
from ....models import random_id, format_date, date
from ...errorHandler import NotFoundException
from .transactionListener import TransactionListener
from datetime import datetime, timedelta
from ....logger import LoggerManager
import math
import asyncio


class TransactionListenerManager(MetaApiClient):
    """Transaction listener manager."""

    def __init__(self, domain_client: DomainClient):
        """Inits transaction listener manager instance.

        Args:
            domain_client: Domain client.
        """
        super().__init__(domain_client)
        self._domainClient = domain_client
        self._strategyTransactionListeners = {}
        self._subscriberTransactionListeners = {}
        self._errorThrottleTime = 1
        self._logger = LoggerManager.get_logger('TransactionListenerManager')

    @property
    def strategy_transaction_listeners(self):
        """Returns the dictionary of strategy transaction listeners.

        Returns:
            Dictionary of strategy transaction listeners.
        """
        return self._strategyTransactionListeners

    @property
    def subscriber_transaction_listeners(self):
        """Returns the dictionary of subscriber transaction listeners.

        Returns:
            Dictionary of subscriber transaction listeners.
        """
        return self._subscriberTransactionListeners

    def add_strategy_transaction_listener(self, listener: TransactionListener, strategy_id: str,
                                          start_time: datetime = None):
        """Adds a strategy transaction listener.

        Args:
            listener: User transaction listener.
            strategy_id: Strategy id.
            start_time: Transaction search start time.

        Returns:
            Strategy transaction listener id.
        """
        listener_id = random_id(10)
        self._strategyTransactionListeners[listener_id] = listener
        asyncio.create_task(self._start_strategy_transaction_stream_job(listener_id, listener, strategy_id,
                                                                        start_time))
        return listener_id

    def add_subscriber_transaction_listener(self, listener: TransactionListener, subscriber_id: str,
                                            start_time: datetime = None):
        """Adds a subscriber transaction listener.

        Args:
            listener: User transaction listener.
            subscriber_id: Subscriber id.
            start_time: Transaction search start time.

        Returns:
            Subscriber transaction listener id.
        """
        listener_id = random_id(10)
        self._subscriberTransactionListeners[listener_id] = listener
        asyncio.create_task(self._start_subscriber_transaction_stream_job(listener_id, listener, subscriber_id,
                                                                          start_time))
        return listener_id

    def remove_strategy_transaction_listener(self, listener_id: str):
        """Removes strategy transaction listener by id.

        Args:
            listener_id: Listener id.
        """
        if listener_id in self._strategyTransactionListeners:
            del self._strategyTransactionListeners[listener_id]

    def remove_subscriber_transaction_listener(self, listener_id: str):
        """Removes subscriber transaction listener by id.

        Args:
            listener_id: Listener id.
        """
        if listener_id in self._subscriberTransactionListeners:
            del self._subscriberTransactionListeners[listener_id]

    async def _start_strategy_transaction_stream_job(self, listener_id: str, listener: TransactionListener,
                                                     strategy_id: str, start_time: datetime = None):
        throttle_time = self._errorThrottleTime
        while listener_id in self._strategyTransactionListeners:
            opts = {
                'url': f'/users/current/strategies/{strategy_id}/transactions/stream',
                'method': 'GET',
                'params': {
                    'limit': 1000
                },
                'headers': {
                    'auth-token': self._token
                }
            }
            if start_time:
                opts['params']['startTime'] = format_date(start_time)
            try:
                packets = await self._domainClient.request_copyfactory(opts, True)
                await listener.on_transaction(packets)
                throttle_time = self._errorThrottleTime
                if listener_id in self._strategyTransactionListeners and len(packets):
                    start_time = date(packets[0]['time']) + timedelta(milliseconds=1)
            except NotFoundException as err:
                await listener.on_error(err)
                self._logger.error(f'Strategy {strategy_id} not found, removing listener f{listener_id}')
                if listener_id in self._strategyTransactionListeners:
                    del self._strategyTransactionListeners[listener_id]
            except Exception as err:
                await listener.on_error(err)
                self._logger.error(f'Failed to retrieve transactions stream for strategy {strategy_id}, ' +
                                   f'listener {listener_id}, retrying in {math.floor(throttle_time)} seconds', err)
                await asyncio.sleep(throttle_time)
                throttle_time = min(throttle_time * 2, 30)

    async def _start_subscriber_transaction_stream_job(self, listener_id: str, listener: TransactionListener,
                                                       subscriber_id: str, start_time: datetime = None):
        throttle_time = self._errorThrottleTime
        while listener_id in self._subscriberTransactionListeners:
            opts = {
                'url': f'/users/current/subscribers/{subscriber_id}/transactions/stream',
                'method': 'GET',
                'params': {
                    'limit': 1000
                },
                'headers': {
                    'auth-token': self._token
                }
            }
            if start_time:
                opts['params']['startTime'] = format_date(start_time)
            try:
                packets = await self._domainClient.request_copyfactory(opts, True)
                await listener.on_transaction(packets)
                throttle_time = self._errorThrottleTime
                if listener_id in self._subscriberTransactionListeners and len(packets):
                    start_time = date(packets[0]['time']) + timedelta(milliseconds=1)
            except NotFoundException as err:
                await listener.on_error(err)
                self._logger.error(f'Subscriber {subscriber_id} not found, removing listener f{listener_id}')
                if listener_id in self._subscriberTransactionListeners:
                    del self._subscriberTransactionListeners[listener_id]
            except Exception as err:
                await listener.on_error(err)
                self._logger.error(f'Failed to retrieve transactions stream for subscriber {subscriber_id}, ' +
                                   f'listener {listener_id}, retrying in {math.floor(throttle_time)} seconds', err)
                await asyncio.sleep(throttle_time)
                throttle_time = min(throttle_time * 2, 30)
