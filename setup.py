import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

install_requires = [
   'aiohttp==3.7.4', 'typing-extensions==3.7.4.3', 'iso8601', 'pytz', 'requests==2.24.0', 'httpx==0.16.1'
]

tests_require = [
      'pytest', 'pytest-mock', 'pytest-asyncio', 'asynctest', 'aiohttp', 'mock', 'freezegun==1.0.0', 'respx==0.16.3'
]

setuptools.setup(
    name="metaapi_cloud_copyfactory_sdk",
    version="3.0.2",
    author="Agilium Labs LLC",
    author_email="agiliumtrade@agiliumtrade.ai",
    description="Python SDK for SDK for CopyFactory trade copying API. Can copy trades both between MetaTrader 5 "
                "(MT5) and MetaTrader 4 (MT4). (https://metaapi.cloud)",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    keywords=['metaapi.cloud', 'MetaTrader', 'MetaTrader 5', 'MetaTrader 4', 'MetaTrader5', 'MetaTrader4', 'MT', 'MT4',
              'MT5', 'forex', 'copy trading', 'API', 'REST', 'client', 'sdk', 'cloud'],
    url="https://github.com/agiliumtrade-ai/copyfactory-python-sdk",
    include_package_data=True,
    package_dir={'metaapi_cloud_copyfactory_sdk': 'lib'},
    packages=['metaapi_cloud_copyfactory_sdk'],
    install_requires=install_requires,
    tests_require=tests_require,
    license='SEE LICENSE IN LICENSE',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)