import asyncio

from collections import deque
from time import time
from uuid import uuid4

from rencode import loads, dumps

GAME_FPS = 30
GAME_TICKER = 1 / GAME_FPS


class Player:
    """docstring for Player"""
    def __init__(self, game_id, id_, address):
        self._id = id_
        self._address = address
        self._game_id = game_id
        self._joined = time()
        self._connected = True
        self._alive = True

    @property
    def address(self):
        return self._address

    @property
    def id(self):
        return self._id

    @property
    def dead(self):
        return not self._alive

    def set_game(self, game_id):
        self._game_id = game_id


class Game:
    """docstring for Game"""
    def __init__(self, id_, transport, *, max_players=2):
        self._id = id_
        self._transport = transport
        self._running = False
        self._epoch = time()
        self._max_players = max_players
        self.players = deque([], self.max_players)

    @property
    def id(self):
        return self._id

    @property
    def max_players(self):
        return self._max_players

    def __len__(self):
        return len(self.players)

    def can_start(self):
        return len(self) >= self.max_players

    def start_game(self):
        start_data = {
            'action': 'start'
        }
        self._running = True
        self.broadcast(start_data)

    def send_message(self, player, message):
        if not isinstance(message, dict):
            return
        message['game_id'] = self.id
        message['timestamp'] = int(time())
        self._transport.sendto(dumps(message), player.address)

    def broadcast(self, message, except_player_id=None):
        for player in self.players:
            if except_player_id != player.id:
                self.send_message(player, message)

    def add_player(self, *args):
        player = Player(self.id, len(self), *args)
        self.players.append(player)
        return player

    def is_running(self):
        return self._running


class Server(asyncio.DatagramProtocol):
    """docstring for Server"""
    def __init__(self):
        self.games = {}
        self.queue = None
        self._transport = None

    def connection_made(self, transport):
        self._transport = transport
        print('connected')

    def connection_lost(self, exc):
        loop = asyncio.get_event_loop()
        loop.stop()
        raise exc

    def parse_packet(self, data):
        data = loads(data)
        return {
            k.decode(): v.decode() if isinstance(v, bytes) else v
            for k, v in data.items()
        }

    def join_game(self, data, addr):
        game = self.get_game()
        player = game.add_player(addr)
        game.send_message(player, {'action': 'joined', 'player_id': player.id})
        if game.can_start():
            self.queue = None
            game.start_game()

    def datagram_received(self, data, addr):
        data = self.parse_packet(data)
        action = data.get('action')
        if action == 'join':
            print(f'receieved join from {addr}')
            self.join_game(data, addr)
        game_id = data.get('game_id')
        game = self.games.get(game_id)

    def transmit(self, message, player):
        self._transport.sendto(message, player.address)

    def generate_id(self):
        return uuid4().hex.upper()

    def get_game(self, *, game_id=None):
        if game_id is not None:
            return self.games.get(game_id)
        if self.queue is not None:
            return self.queue
        game_id = self.generate_id()
        self.queue = game = Game(game_id, self._transport)
        self.games[game_id] = game
        return game


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_datagram_endpoint(
        Server,
        local_addr=('127.0.0.1', 9999)
    )
    transport, protocol = loop.run_until_complete(task)
    loop.run_forever()
    transport.close()
    loop.close()
