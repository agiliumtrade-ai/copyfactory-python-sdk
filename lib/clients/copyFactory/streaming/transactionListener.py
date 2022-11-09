from abc import abstractmethod
from ..copyFactory_models import CopyFactoryTransaction
from typing import List


class TransactionListener:
    """Transaction listener for handling a stream of transaction events."""

    @abstractmethod
    async def on_transaction(self, transaction_event: List[CopyFactoryTransaction]):
        """Calls a predefined function with the packets data.

        Args:
            transaction_event: Transaction event with an array of packets.
        """
        pass

    async def on_error(self, error: Exception):
        """Calls a predefined function with the received error.

        Args:
            error: Error received during retrieve attempt.
        """
        pass
