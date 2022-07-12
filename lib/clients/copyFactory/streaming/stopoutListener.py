from abc import abstractmethod
from ..copyFactory_models import CopyFactoryStrategyStopout
from typing import List


class StopoutListener:
    """Stopout listener for handling a stream of stopout events."""

    @abstractmethod
    async def on_stopout(self, strategy_stopout_event: List[CopyFactoryStrategyStopout]):
        """Calls a predefined function with the packets data.

        Args:
            strategy_stopout_event: Strategy stopout event with an array of packets.
        """
        pass
