import asyncio
import os
import signal
from nats.aio.client import Client as NATS


def add_subscription(loop):
    nc = NATS()

    @asyncio.coroutine
    def closed_cb():
        print("Connection to NATS is closed.")
        yield from asyncio.sleep(0.1, loop=loop)
        loop.stop()

    options = {
        "servers": ["nats://127.0.0.1:4222"],
        "io_loop": loop,
        "closed_cb": closed_cb
    }

    yield from nc.connect(**options)
    print("Connected to NATS at {}...".format(nc.connected_url.netloc))

    # PUBLISH
    print('Publishing some stuff.')
    yield from nc.publish('cc-subscriptions',
                          b'5~CCCAGG~ETH~USD, 5~CCCAGG~BTC~USD')

    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

    @asyncio.coroutine
    def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    yield from nc.subscribe('crypto-compare', cb=message_handler)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_subscription(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()


