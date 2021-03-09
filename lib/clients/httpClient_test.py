from .httpClient import HttpClient
import re
import pytest
import respx
import asyncio
from httpx import Response, ConnectTimeout, Request
from .errorHandler import ApiException
httpClient = None
test_url = 'http://example.com'


@pytest.fixture(autouse=True)
async def run_around_tests():
    global httpClient
    httpClient = HttpClient(retry_opts={'minDelayInSeconds': 0.05, 'maxDelayInSeconds': 0.2})
    yield


class TestHttpClient:
    @pytest.mark.asyncio
    async def test_load(self):
        """Should load HTML page from example.com"""
        opts = {
            'url': test_url
        }
        response = await httpClient.request(opts)
        text = response.text
        assert re.search('doctype html', text)

    @pytest.mark.asyncio
    async def test_not_found(self):
        """Should return NotFound exception if server returns 404"""
        opts = {
            'url': f'{test_url}/not-found'
        }
        try:
            await httpClient.request(opts)
            raise Exception('NotFoundException is expected')
        except Exception as err:
            assert err.__class__.__name__ == 'NotFoundException'

    @pytest.mark.asyncio
    async def test_timeout(self):
        """Should return ConnectTimeout exception if request is timed out"""
        httpClient = HttpClient(0.001, {'retries': 2, 'minDelayInSeconds': 0.05, 'maxDelayInSeconds': 0.2})
        opts = {
            'url': test_url
        }
        try:
            await httpClient.request(opts)
            raise Exception('ConnectTimeout is expected')
        except Exception as err:
            assert err.__class__.__name__ == 'ConnectTimeout'

    @respx.mock
    @pytest.mark.asyncio
    async def test_validation_exception(self):
        """Should return a validation exception"""
        error = {
            'id': 1,
            'error': 'error',
            'message': 'test message',
        }
        respx.post(test_url).mock(return_value=Response(400, json=error))
        opts = {
            'method': 'POST',
            'url': test_url
        }
        try:
            await httpClient.request(opts)
            raise Exception('ValidationException is expected')
        except Exception as err:
            assert err.__class__.__name__ == 'ValidationException'
            assert err.__str__() == 'test message, check error.details for more information'

    @respx.mock
    @pytest.mark.asyncio
    async def test_validation_exception_details(self):
        """Should return a validation exception with details"""
        error = {
            'id': 1,
            'error': 'error',
            'message': 'test',
            'details': [{'parameter': 'password', 'value': 'wrong', 'message': 'Invalid value'}]
        }
        respx.post(test_url).mock(return_value=Response(400, json=error))
        opts = {
            'method': 'POST',
            'url': test_url
        }
        try:
            await httpClient.request(opts)
            raise Exception('ValidationException is expected')
        except Exception as err:
            assert err.__class__.__name__ == 'ValidationException'
            assert err.__str__() == 'test, check error.details for more information'
            assert err.details == error['details']

    @respx.mock
    @pytest.mark.asyncio
    async def test_retry_on_fail(self):
        """Should retry request on fail."""
        opts = {
            'method': 'POST',
            'url': test_url
        }
        respx.post(test_url).mock(side_effect=[ConnectTimeout('test', request=Request('GET', opts['url'])),
                                               ConnectTimeout('test', request=Request('GET', opts['url'])),
                                               Response(200, text='response')])
        response = await httpClient.request(opts)
        assert response.text == 'response'

    @respx.mock
    @pytest.mark.asyncio
    async def test_return_error_on_retry_limit_exceeded(self):
        """Should return error if retry limit exceeded."""
        opts = {
            'method': 'POST',
            'url': test_url
        }
        respx.post(test_url).mock(side_effect=ConnectTimeout)
        try:
            await httpClient.request(opts)
            raise Exception('ConnectTimeout is expected')
        except Exception as err:
            assert err.__class__.__name__ == 'ConnectTimeout'

    @respx.mock
    @pytest.mark.asyncio
    async def test_not_retry_if_error_not_specified(self):
        """Should not retry if error not specified."""
        error = {
            'id': 1,
            'error': 'error',
            'message': 'test',
            'details': [{'parameter': 'password', 'value': 'wrong', 'message': 'Invalid value'}]
        }
        respx.post(test_url).mock(side_effect=[Response(400, json=error), Response(400, json=error), Response(204)])
        opts = {
            'method': 'POST',
            'url': test_url
        }
        try:
            await httpClient.request(opts)
            raise Exception('ValidationException is expected')
        except Exception as err:
            assert err.__class__.__name__ == 'ValidationException'
            assert err.__str__() == 'test, check error.details for more information'
            assert err.details == error['details']
