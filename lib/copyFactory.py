from .clients.httpClient import HttpClient
from .clients.copyFactory.configuration_client import ConfigurationClient
from .clients.copyFactory.history_client import HistoryClient
from .clients.copyFactory.trading_client import TradingClient
from typing_extensions import TypedDict
from typing import Optional


class RetryOpts(TypedDict):
    retries: Optional[int]
    """Maximum amount of request retries, default value is 5."""
    minDelayInSeconds: Optional[float]
    """Minimum delay in seconds until request retry, default value is 1."""
    maxDelayInSeconds: Optional[float]
    """Maximum delay in seconds until request retry, default value is 30."""


class CopyFactoryOpts(TypedDict):
    """CopyFactory options"""
    domain: str
    """Domain to connect to."""
    requestTimeout: float
    """Timeout for http requests in seconds."""
    retryOpts: Optional[RetryOpts]
    """Options for request retries."""


class CopyFactory:
    """MetaApi CopyFactory copy trading API SDK"""

    def __init__(self, token: str, opts: CopyFactoryOpts = None):
        """Inits CopyFactory class instance.

        Args:
            token: Authorization token.
            opts: Connection options.
        """
        opts: CopyFactoryOpts = opts or {}
        domain = opts['domain'] if 'domain' in opts else 'agiliumtrade.agiliumtrade.ai'
        request_timeout = opts['requestTimeout'] if 'requestTimeout' in opts else 60
        retry_opts = opts['retryOpts'] if 'retryOpts' in opts else {}
        http_client = HttpClient(request_timeout, retry_opts)
        self._configurationClient = ConfigurationClient(http_client, token, domain)
        self._historyClient = HistoryClient(http_client, token, domain)
        self._tradingClient = TradingClient(http_client, token, domain)

    @property
    def configuration_api(self) -> ConfigurationClient:
        """Returns CopyFactory configuration API.

        Returns:
            Configuration API.
        """
        return self._configurationClient

    @property
    def history_api(self) -> HistoryClient:
        """Returns CopyFactory history API.

        Returns:
            History API.
        """
        return self._historyClient

    @property
    def trading_api(self) -> TradingClient:
        """Returns CopyFactory history API.

        Returns:
            History API.
        """
        return self._tradingClient
