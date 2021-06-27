import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk import CopyFactory

# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'
# your master MetaApi account id
master_account_id = os.getenv('MASTER_ACCOUNT_ID') or '<put in your masterAccountId here>'
# your slave MetaApi account id
slave_account_id = os.getenv('SLAVE_ACCOUNT_ID') or '<put in your slaveAccountId here>'


async def configure_copyfactory():
    api = MetaApi(token)
    copy_factory = CopyFactory(token)

    try:
        global master_account_id
        global slave_account_id
        accounts = await api.metatrader_account_api.get_accounts()
        master_metaapi_account = next((a for a in accounts if a.id == master_account_id), None)
        if (not hasattr(master_metaapi_account, 'application')) or master_metaapi_account.application != 'CopyFactory':
            raise Exception('Please specify CopyFactory application field value in your MetaApi '
                            'account in order to use it in CopyFactory API')

        slave_metaapi_account = next((a for a in accounts if a.id == slave_account_id), None)
        if (not hasattr(slave_metaapi_account, 'application')) or slave_metaapi_account.application != 'CopyFactory':
            raise Exception('Please specify CopyFactory application field value in your MetaApi '
                            'account in order to use it in CopyFactory API')

        configuration_api = copy_factory.configuration_api
        copyfactory_accounts = await configuration_api.get_accounts()
        master_account = next((a for a in copyfactory_accounts if a['connectionId'] == master_metaapi_account.id),
                              None)
        if master_account:
            master_account_id = master_account['_id']
        else:
            master_account_id = configuration_api.generate_account_id()
        await configuration_api.update_account(master_account_id, {
            'name': 'Demo master account',
            'connectionId': master_metaapi_account.id,
            'subscriptions': []
        })

        strategies = await configuration_api.get_strategies()
        strategy = next((a for a in strategies if a['connectionId'] == master_metaapi_account.id),
                        None)
        if strategy:
            strategy_id = strategy['_id']
        else:
            strategy_id = await configuration_api.generate_strategy_id()
            strategy_id = strategy_id['id']

        # create a strategy being copied
        await configuration_api.update_strategy(strategy_id, {
            'name': 'Test strategy',
            'description': 'Some useful description about your strategy',
            'connectionId': master_metaapi_account.id
        })
        slave_account = next((a for a in copyfactory_accounts if a['connectionId'] == slave_metaapi_account.id),
                             None)
        if slave_account:
            await configuration_api.remove_account(slave_account['_id'])
        slave_account_id = configuration_api.generate_account_id()

        # subscribe slave CopyFactory accounts to the strategy
        await configuration_api.update_account(slave_account_id, {
            'name': 'Demo slave account',
            'connectionId': slave_metaapi_account.id,
            'subscriptions': [
                {
                    'strategyId': strategy_id,
                    'multiplier': 1
                }
            ]
        })

        print('Please note that it can take some time for CopyFactory to initialize accounts. During this time the '
              'MetaApi accounts may redeploy a couple of times. After initialization finishes, you can copy trades '
              'from your master to slave account.')
    except Exception as err:
        print(api.format_error(err))


asyncio.run(configure_copyfactory())
