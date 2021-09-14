CopyFactory trade copying API for Python (a member of `metaapi.cloud <https://metaapi.cloud>`_ project)
#######################################################################################################

CopyFactory is a powerful trade copying API which makes developing forex
trade copying applications as easy as writing few lines of code.

CopyFactory API is a member of MetaApi project (`https://metaapi.cloud <https://metaapi.cloud>`_),
a powerful cloud forex trading API which supports both MetaTrader 4 and MetaTrader 5 platforms.

MetaApi is a paid service, however API access to one MetaTrader account is free of charge.

The `MetaApi pricing <https://metaapi.cloud/#pricing>`_ was developed with the intent to make your charges less or equal to what you would have to pay
for hosting your own infrastructure. This is possible because over time we managed to heavily optimize
our MetaTrader infrastructure. And with MetaApi you can save significantly on application development and
maintenance costs and time thanks to high-quality API, open-source SDKs and convenience of a cloud service.

Why do we offer CopyFactory API trade copying API
=================================================

We found that developing reliable and flexible trade copier is a task
which requires lots of effort, because developers have to solve a series
of complex technical tasks to create a product.

We decided to share our product as it allows developers to start with a
powerful solution in almost no time, saving on development and
infrastructure maintenance costs.

Frequently asked questions (FAQ)
================================

FAQ is located here: `http://metaapi.cloud/docs/copyfactory/faq <http://metaapi.cloud/docs/copyfactory/faq>`_

CopyFactory copytrading API features
====================================

Features supported:

- low latency trade copying API
- reliable trade copying API
- suitable for large-scale deployments
- suitable for large number of subscribers
- connect arbitrary number of strategy providers and subscribers
- subscribe accounts to multiple strategies at once
- select arbitrary copy ratio for each subscription
- configure symbol mapping between strategy providers and subscribers
- apply advanced risk filters on strategy provider side
- override risk filters on subscriber side
- provide multiple strategies from a single account based on magic or symbol filters
- supports manual trading on subscriber accounts while copying trades
- synchronize subscriber account with strategy providers
- monitor trading history
- calculate trade copying commissions for account managers
- support portfolio strategies as trading signal source, i.e. the strategies which include signals of several other strategies (also known as combos on some platforms)

Please note that trade copying to MT5 netting accounts is not supported in the current API version

Please check Features section of the `https://metaapi.cloud/docs/copyfactory/ <https://metaapi.cloud/docs/copyfactory/>`_
documentation for detailed description of all settings you can make.

REST API documentation
======================

CopyFactory SDK is built on top of CopyFactory REST API.

CopyFactory REST API docs are available at `https://metaapi.cloud/docs/copyfactory/ <https://metaapi.cloud/docs/copyfactory/>`_

Code examples
=============

We published some code examples in our github repository, namely:

- Python: `https://github.com/agiliumtrade-ai/copyfactory-python-sdk/tree/master/examples <https://github.com/agiliumtrade-ai/copyfactory-python-sdk/tree/master/examples>`_

Installation
============

.. code-block:: bash

    pip install metaapi-cloud-sdk

Retrieving API token
====================

Please visit `https://app.metaapi.cloud/token <https://app.metaapi.cloud/token>`_ web UI to obtain your API token.

Configuring trade copying
=========================

In order to configure trade copying you need to:

- add MetaApi MetaTrader accounts with CopyFactory as application field value (see above)
- create CopyFactory master and slave accounts and connect them to MetaApi accounts via connectionId field
- create a strategy being copied
- subscribe slave CopyFactory accounts to the strategy

.. code-block:: python

    from metaapi_cloud_sdk import MetaApi, CopyFactory

    token = '...'
    metaapi = MetaApi(token=token)
    copy_factory = CopyFactory(token=token)

    # retrieve MetaApi MetaTrader accounts with CopyFactory as application field value
    # master account must have PROVIDER value in copyFactoryRoles
    master_metaapi_account = await metaapi.metatrader_account_api.get_account(account_id='masterMetaapiAccountId')
    if (master_metaapi_account is None) or master_metaapi_account.copy_factory_roles is None or 'PROVIDER' not \
            in master_metaapi_account.copy_factory_roles:
        raise Exception('Please specify PROVIDER copyFactoryRoles value in your MetaApi '
                        'account in order to use it in CopyFactory API')
    # slave account must have SUBSCRIBER value in copyFactoryRoles
    slave_metaapi_account = await metaapi.metatrader_account_api.get_account(account_id='slaveMetaapiAccountId')
    if (slave_metaapi_account is None) or slave_metaapi_account.copy_factory_roles is None or 'SUBSCRIBER' not \
            in slave_metaapi_account.copy_factory_roles:
        raise Exception('Please specify SUBSCRIBER copyFactoryRoles value in your MetaApi '
                        'account in order to use it in CopyFactory API')

    configuration_api = copy_factory.configuration_api

    # create a strategy being copied
    strategy_id = await configuration_api.generate_strategy_id()
    await configuration_api.update_strategy(id=strategy_id['id'], strategy={
        'name': 'Test strategy',
        'description': 'Some useful description about your strategy',
        'positionLifecycle': 'hedging',
        'accountId': master_metaapi_account.id,
        'maxTradeRisk': 0.1,
        'stopOutRisk': {
            'value': 0.4,
            'startTime': '2020-08-24T00:00:00.000Z'
        },
        'timeSettings': {
            'lifetimeInHours': 192,
            'openingIntervalInMinutes': 5
        }
    })

    # subscribe slave CopyFactory accounts to the strategy
    await configuration_api.update_subscriber(slave_metaapi_account.id, {
        'name': 'Demo account',
        'subscriptions': [
            {
                'strategyId': strategy_id['id'],
                'multiplier': 1
            }
        ]
    })

    # retrieve list of strategies
    print(await configuration_api.get_strategies())

    # retrieve list of provider portfolios
    print(await configuration_api.get_portfolio_strategies())

    # retrieve list of subscribers
    print(await configuration_api.get_subscribers())

See in-code documentation for full definition of possible configuration options.

Retrieving trade copying history
================================

CopyFactory allows you to monitor transactions conducted on trading accounts in real time.

Retrieving trading history on provider side
-------------------------------------------

.. code-block:: python

    history_api = copy_factory.history_api

    # retrieve trading history, please note that this method support pagination and limits number of records
    print(await history_api.get_provided_transactions(time_from=datetime.fromisoformat('2020-08-01'),
        time_till=datetime.fromisoformat('2020-09-01')))


Retrieving trading history on subscriber side
---------------------------------------------

.. code-block:: python

    history_api = copy_factory.history_api

    # retrieve trading history, please note that this method support pagination and limits number of records
    print(await history_api.get_subscription_transactions(time_from=datetime.fromisoformat('2020-08-01'),
        time_till=datetime.fromisoformat('2020-09-01')))

Resynchronizing slave accounts to masters
=========================================
There is a configurable time limit during which the trades can be opened. Sometimes trades can not open in time due to broker errors or trading session time discrepancy.
You can resynchronize a slave account to place such late trades. Please note that positions which were
closed manually on a slave account will also be reopened during resynchronization.

.. code-block:: python

    account_id = '...' # CopyFactory account id

    # resynchronize all strategies
    await copy_factory.trading_api.resynchronize(account_id=account_id)

    # resynchronize specific strategy
    await copy_factory.trading_api.resynchronize(account_id=account_id, strategy_ids=['ABCD'])

Sending external trading signals to a strategy
==============================================
You can submit external trading signals to your trading strategy.

.. code-block:: python

    trading_api = copy_factory.trading_api
    signal_id = trading_api.generate_signal_id()

    # add trading signal
    await trading_api.update_external_signal(strategy_id=strategy_id, signal_id=signal_id, signal={
        'symbol': 'EURUSD',
        'type': 'POSITION_TYPE_BUY',
        'time': datetime.now(),
        'volume': 0.01
    })

    # remove signal
    await trading_api.remove_external_signal(strategy_id=strategy_id, signal_id=signal_id, signal={
        'time': datetime.now()
    })

Retrieving trading signals
==========================

.. code-block:: python

    subscriber_id = '...' # CopyFactory subscriber id

    # retrieve trading signals
    print(await copy_factory.trading_api.get_trading_signals(subscriber_id))

Managing stopouts
=================
A subscription to a strategy can be stopped if the strategy have exceeded allowed risk limit.

.. code-block:: python

    trading_api = copy_factory.trading_api
    account_id = '...' # CopyFactory account id
    strategy_id = '...' # CopyFactory strategy id

    # retrieve list of strategy stopouts
    print(await trading_api.get_stopouts(account_id=account_id))

    # reset a stopout so that subscription can continue
    await trading_api.reset_stopouts(account_id=account_id, strategy_id=strategy_id, reason='daily-equity')

Retrieving slave trading logs
=============================

.. code-block:: python

    trading_api = copy_factory.trading_api
    account_id = '...' # CopyFactory account id

    # retrieve slave trading log
    print(await trading_api.get_user_log(account_id))

    # retrieve paginated slave trading log by time range
    print(await trading_api.get_user_log(account_id, datetime.fromtimestamp(datetime.now().timestamp() - 24 * 60 * 60), None, 20, 10))

Related projects:
=================

See our website for the full list of APIs and features supported `https://metaapi.cloud/#features <https://metaapi.cloud/#features>`_

Some of the APIs you might decide to use together with this module:

1. MetaApi cloud forex trading API `https://metaapi.cloud/docs/client/ <https://metaapi.cloud/docs/client/>`_
2. MetaStats cloud forex trading statistics API `https://metaapi.cloud/docs/metastats/ <https://metaapi.cloud/docs/metastats/>`_
