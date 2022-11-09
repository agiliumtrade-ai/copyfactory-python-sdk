import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk import CopyFactory, TransactionListener


# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'

# your subscriber id
subscriber_id = os.getenv('SUBSCRIBER_ID') or '<put in your subscriber id here>'

copyfactory = CopyFactory(token)


class Listener(TransactionListener):
    async def on_transaction(self, transaction_event):
        print('Transaction event', transaction_event)

    async def on_error(self, error: Exception):
        print('Error event', error)


async def transaction_listener_example():
    api = MetaApi(token)
    try:
        listener = Listener()

        history_api = copyfactory.history_api
        listener_id = history_api.add_subscriber_transaction_listener(listener, subscriber_id)
        await asyncio.sleep(300)
        history_api.remove_subscriber_transaction_listener(listener_id)
    except Exception as err:
        print(api.format_error(err))

asyncio.run(transaction_listener_example())
