import asyncio
import logging

from rencode import loads, dumps

logger = logging.getLogger('laser-snake.client')
logger.setLevel(logging.DEBUG)


def write_to_file(line):
    with open('f', 'a+') as fp:
        fp.write(str(line) + '\n')


class Client(asyncio.DatagramProtocol):
    """docstring for Client"""
    def __init__(self):
        self._transport = None

    def connection_made(self, transport):
        self._transport = transport
        req = {
            'action': 'join',
            'x': 123,
            'y': list(range(5))
        }
        self._transport.sendto(
            dumps(req)
        )

    def connection_lost(self, exc):
        loop = asyncio.get_event_loop()
        loop.stop()
        raise exc

    def error_received(self, exc):
        raise exc

    def parse_packet(self, data):
        data = loads(data)
        return {
            k.decode(): v.decode() if isinstance(v, bytes) else v
            for k, v in data.items()
        }

    def datagram_received(self, data, addr):
        data = self.parse_packet(data)
        action = data.get('action')
        game_id = data.get('game_id')
        logger.info(data)
        write_to_file(data)
        if None in (game_id, action):
            return


if __name__ == "__main__":
    print('hey')
    loop = asyncio.get_event_loop()
    listener = loop.create_datagram_endpoint(
        Client,
        remote_addr=('127.0.0.1', 9999)
    )
    transport, protocol = loop.run_until_complete(listener)
    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        transport.close()
        loop.close()
