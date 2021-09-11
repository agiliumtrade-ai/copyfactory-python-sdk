import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from lib import CopyFactory
from datetime import datetime

# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'
# your master MetaApi account id
# master account must have PROVIDER value in copyFactoryRoles
master_account_id = os.getenv('MASTER_ACCOUNT_ID') or '<put in your masterAccountId here>'
# your slave MetaApi account id
# slave account must have SUBSCRIBER value in copyFactoryRoles
slave_account_id = os.getenv('SLAVE_ACCOUNT_ID') or '<put in your slaveAccountId here>'


async def external_signal():
    api = MetaApi(token)
    copy_factory = CopyFactory(token)

    try:
        master_metaapi_account = await api.metatrader_account_api.get_account(master_account_id)
        if (master_metaapi_account is None) or master_metaapi_account.copy_factory_roles is None or 'PROVIDER' not \
                in master_metaapi_account.copy_factory_roles:
            raise Exception('Please specify PROVIDER copyFactoryRoles value in your MetaApi '
                            'account in order to use it in CopyFactory API')
        slave_metaapi_account = await api.metatrader_account_api.get_account(slave_account_id)
        if (slave_metaapi_account is None) or slave_metaapi_account.copy_factory_roles is None or 'SUBSCRIBER' not \
                in slave_metaapi_account.copy_factory_roles:
            raise Exception('Please specify SUBSCRIBER copyFactoryRoles value in your MetaApi '
                            'account in order to use it in CopyFactory API')

        configuration_api = copy_factory.configuration_api
        strategies = await configuration_api.get_strategies()
        strategy = next((s for s in strategies if s['accountId'] == master_metaapi_account.id), None)
        if strategy:
            strategy_id = strategy['_id']
        else:
            strategy_id = await configuration_api.generate_strategy_id()
            strategy_id = strategy_id['id']

        # create a strategy
        await configuration_api.update_strategy(strategy_id, {
            'name': 'Test strategy',
            'description': 'Some useful description about your strategy',
            'accountId': master_metaapi_account.id
        })

        # create subscriber
        await configuration_api.update_subscriber(slave_metaapi_account.id, {
            'name': 'Test subscriber',
            'subscriptions': [
                {
                    'strategyId': strategy_id,
                    'multiplier': 1
                }
            ]
        })

        # send external signal
        trading_api = copy_factory.trading_api
        signal_id = trading_api.generate_signal_id()
        await trading_api.update_external_signal(strategy_id=strategy_id, signal_id=signal_id, signal={
            'symbol': 'EURUSD',
            'type': 'POSITION_TYPE_BUY',
            'time': datetime.now(),
            'volume': 0.01
        })

        await asyncio.sleep(10)

        # output trading signals
        print(await trading_api.get_trading_signals(slave_metaapi_account.id))

        # remove external signal
        await trading_api.remove_external_signal(strategy_id=strategy_id, signal_id=signal_id, signal={
            'time': datetime.now()
        })
    except Exception as err:
        print(api.format_error(err))


asyncio.run(external_signal())
