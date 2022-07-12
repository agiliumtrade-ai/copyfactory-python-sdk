from abc import abstractmethod
from ..copyFactory_models import CopyFactoryUserLogMessage
from typing import List


class UserLogListener:
    """User log listener for handling a stream of transaction events."""

    @abstractmethod
    async def on_user_log(self, log_event: List[CopyFactoryUserLogMessage]):
        """Calls a predefined function with the packets data.

        Args:
            log_event: User log event with an array of packets.
        """
        pass
