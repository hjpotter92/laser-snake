import asyncio
import logging

from rencode import loads, dumps

from enums import Direction
from game import SnakeGame
from utils import TIME, parse_packet

FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('laser-snake.client')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('client.log'))


class Client(asyncio.DatagramProtocol):
    """docstring for Client"""
    def __init__(self):
        self._transport = None
        self._game_id = None
        self._player_id = None
        self.started = False
        self.game = None

    @property
    def game_id(self):
        return self._game_id

    @property
    def player_id(self):
        return self._player_id

    def connection_made(self, transport):
        self._transport = transport
        req = {
            'action': 'join',
            'x': 123,
            'y': list(range(5))
        }
        self.send_message(req)

    def connection_lost(self, exc):
        loop = asyncio.get_event_loop()
        loop.stop()
        raise exc

    def error_received(self, exc):
        raise exc

    def send_message(self, message):
        if not isinstance(message, dict):
            return
        message['game_id'] = self.game_id
        message['player_id'] = self.player_id
        self._transport.sendto(dumps(message))

    def set_game(self, data):
        self.game = SnakeGame(client=self, **data)
        self._game_id = data.get('game_id')
        self._player_id = data.get('player_id')
        logger.debug(data)

    def start_game(self, data):
        def executor():
            game = self.game
            game.run(**data)
            game.quit()
        if self.started is True:
            return
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, executor)
        self.started = True

    def datagram_received(self, data, addr):
        data = parse_packet(data)
        action = data.get('action')
        if action is None:
            return
        if action == 'error':
            logger.error(data.get('error'))
            return
        game_id = data.get('game_id')
        player_id = data.get('player_id')
        if action == 'joined':
            self.set_game(data)
            return
        if self.game_id != game_id:
            logger.error("Wrong game_id detected")
            return
        if action == 'start' and self.started is False:
            logger.info(f"Starting game at {TIME()}")
            self.start_game(data)
            return
        if action == 'objects':
            self.game.parse_snakes(data.get('snakes'))
            self.game.foods = data.get('foods')
        elif action == 'over':
            logger.debug(data)
            self.game.over()


if __name__ == "__main__":
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
