from .errorHandler import UnauthorizedException, ForbiddenException, ApiException, ConflictException, \
    ValidationException, InternalException, NotFoundException, TooManyRequestsException
from typing_extensions import TypedDict
from typing import Optional
from ..models import ExceptionMessage
import json
import asyncio
import sys
import httpx
from httpx import HTTPError, Response


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class RequestOptions(TypedDict):
    """Options for HttpClient requests."""
    method: Optional[str]
    url: str
    headers: Optional[dict]
    params: Optional[dict]
    body: Optional[dict]
    files: Optional[dict]


class HttpClient:
    """HTTP client library based on requests module."""
    def __init__(self, timeout: float = 60, retry_opts=None):
        """Inits HttpClient class instance.

        Args:
            timeout: Request timeout in seconds.
        """
        if retry_opts is None:
            retry_opts = {}
        self._timeout = timeout
        self._retries = retry_opts['retries'] if 'retries' in retry_opts else 5
        self._minRetryDelayInSeconds = retry_opts['minDelayInSeconds'] if 'minDelayInSeconds' in retry_opts else 1
        self._maxRetryDelayInSeconds = retry_opts['maxDelayInSeconds'] if 'maxDelayInSeconds' in retry_opts else 30

    async def request(self, options: RequestOptions, retry_counter: int = 0) -> Response:
        """Performs a request. Response errors are returned as ApiError or subclasses.

        Args:
            options: Request options.

        Returns:
            A request response.
        """
        try:
            response = await self._make_request(options)
            response.raise_for_status()
            if response.content:
                try:
                    response = response.json()
                except Exception as err:
                    print('Error parsing json', err)
        except HTTPError as err:
            if err.__class__.__name__ == 'ConnectTimeout':
                error = err
            else:
                error = self._convert_error(err)
            if error.__class__.__name__ in ['ConflictException', 'InternalException', 'ApiException', 'ConnectTimeout']\
                    and retry_counter < self._retries:
                await asyncio.sleep(min(pow(2, retry_counter) * self._minRetryDelayInSeconds,
                                        self._maxRetryDelayInSeconds))
                return await self.request(options, retry_counter + 1)
            else:
                raise error
        return response

    async def _make_request(self, options: RequestOptions) -> Response:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            method = options['method'] if ('method' in options) else 'GET'
            url = options['url']
            params = options['params'] if 'params' in options else None
            files = options['files'] if 'files' in options else None
            headers = options['headers'] if 'headers' in options else None
            body = options['body'] if 'body' in options else None
            req = client.build_request(method, url, params=params, files=files, headers=headers, json=body)
            response = await client.send(req)
            return response

    def _convert_error(self, err: HTTPError):
        try:
            response: ExceptionMessage or TypedDict = json.loads(err.response.text)
        except Exception:
            response = {}
        err_message = response['message'] if 'message' in response else err.response.reason_phrase
        status = err.response.status_code
        if status == 400:
            details = response['details'] if 'details' in response else []
            return ValidationException(err_message, details)
        elif status == 401:
            return UnauthorizedException(err_message)
        elif status == 403:
            return ForbiddenException(err_message)
        elif status == 404:
            return NotFoundException(err_message)
        elif status == 409:
            return ConflictException(err_message)
        elif status == 429:
            err_metadata = response['metadata'] if 'metadata' in response else {}
            return TooManyRequestsException(err_message, err_metadata)
        elif status == 500:
            return InternalException(err_message)
        else:
            return ApiException(err_message, status)
