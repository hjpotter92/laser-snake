import asyncio

from collections import deque
from math import log10
from random import choice, randint
from uuid import uuid4

from rencode import dumps

from enums import Direction
from food import Food
from snake import Snake
from utils import TIME, parse_packet
from vector import Vector, random_vector

GAME_FPS = 30
GAME_TICKER = 1 / GAME_FPS


class Player:
    """docstring for Player"""
    def __init__(self, game_id, id_, address, **kwds):
        self._id = id_
        self._address = address
        self._game_id = game_id
        self._joined = TIME()
        self._connected = True
        self._alive = True
        self.boundary = kwds.get('boundary')
        self.next_direction = Direction.RANDOM()
        self.snake = None

    @property
    def address(self):
        return self._address

    @property
    def id(self):
        return self._id

    @property
    def dead(self):
        return not self.alive

    @property
    def alive(self):
        return self._alive

    @property
    def topleft(self):
        return self.boundary[0]

    @property
    def bottomright(self):
        return self.boundary[1]

    @property
    def direction(self):
        if self.snake is None:
            return self.next_direction.value
        return self.snake.direction

    @direction.setter
    def direction(self, value):
        if not isinstance(value, Direction):
            raise TypeError("enum expected")
        self.next_direction = value

    def snake_packet(self):
        return {
            'head': tuple(self.snake.head),
            'segments': self.snake.blocks,
            'direction': Direction(self.direction).name,
            'player': {
                'id': self.id,
                'alive': not self.dead
            }
        }

    def inside_boundary(self, point):
        return (
            self.topleft[0] <= point[0] <= self.bottomright[0] and
            self.topleft[1] <= point[1] <= self.bottomright[1]
        )

    def set_game(self, game_id):
        self._game_id = game_id

    def attach_snake(self, snake):
        self.snake = snake

    def check_bounds(self):
        if not self.inside_boundary(self.snake.head):
            self.snake.loop(*self.boundary)

    def update(self, δt):
        self.snake.update(δt, self.next_direction.value)


class Game:
    """docstring for Game"""
    def __init__(self, id_, transport, loop, max_players=2, world_size=None):
        self._id = id_
        self._transport = transport
        self._running = False
        self._epoch = TIME()
        self._max_players = max_players
        self.loop = loop
        self.foods = set()
        self.world_size = world_size or (16, 16)
        self.players = deque([], self.max_players)

    @property
    def id(self):
        return self._id

    @property
    def max_players(self):
        return self._max_players

    @property
    def boundary(self):
        return (
            (0, 0),
            self.world_size - Direction.BOTTOM_RIGHT.value
        )

    def __len__(self):
        return len(self.players)

    def get_player(self, player_id):
        player = self.players[player_id]
        if player.id == player_id:
            return player
        return next(
            (player for player in self.players if player.id == player_id)
        )

    def get_tick(self):
        last_tick = self.loop.time()

        def wrapped():
            nonlocal last_tick
            δt = self.loop.time() - last_tick
            last_tick = self.loop.time()
            return δt
        return wrapped

    def is_running(self):
        return self._running

    def can_start(self):
        return len(self) >= self.max_players

    def send_message(self, player, message):
        if not isinstance(message, dict):
            return
        message['game_id'] = self.id
        message['player_id'] = player.id
        message['timestamp'] = TIME()
        self._transport.sendto(dumps(message), player.address)

    def broadcast(self, message, except_player_id=None):
        for player in self.players:
            if except_player_id != player.id:
                self.send_message(player, message)

    def broadcast_error(self, message, except_player_id=None):
        error_data = {
            'action': 'error',
            'error': message
        }
        self.broadcast(error_data, except_player_id)

    def generate_snake(self, player):
        snakes = [
            p.snake for p in self.players
            if p != player and p.snake is not None
        ]
        exceptions = []
        for snake in snakes:
            exceptions += snake.blocks
        pos = random_vector(*self.boundary, exceptions=exceptions)
        player.snake = snake = Snake(pos, player.direction)
        return snake

    def generate_food(self):
        exceptions = []
        for player in self.players:
            exceptions += player.snake.blocks
        for food in self.foods:
            exceptions += food.position
        position = random_vector(
            *self.boundary,
            exceptions=exceptions
        )
        rand = randint(2, 9999)
        score = int(3 / log10(rand)) + 1
        self.foods.add(Food(position, score))

    def add_player(self, *args):
        player = Player(self.id, len(self), *args, boundary=self.boundary)
        snake = self.generate_snake(player)
        self.players.append(player)
        return player

    def start_game(self):
        start_data = {
            'action': 'start',
            'world_size': self.world_size,
            'snakes': [player.snake_packet() for player in self.players]
        }
        self.generate_food()
        self._running = True
        self.broadcast(start_data)
        self.loop.create_task(self.run(GAME_TICKER))

    def update(self, δt):
        for player in self.players:
            player.update(δt)
            player.check_bounds()
        self.broadcast({
            'action': 'objects',
            'snakes': [player.snake_packet() for player in self.players],
            'foods': [food.packet() for food in self.foods]
        })

    async def run(self, ticker):
        await asyncio.sleep(1)
        while self.is_running():
            tick = await asyncio.sleep(ticker, result=self.get_tick())
            δt = tick()
            self.update(δt)

    def process_action(self, action, data):
        if action == "move":
            player = self.get_player(data.get('player_id'))
            player.direction = Direction[data.get('direction').upper()]


class Server(asyncio.DatagramProtocol):
    """docstring for Server"""
    def __init__(self, loop):
        self.loop = loop
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

    def send_error(self, addr, message):
        error_data = {
            'action': 'error',
            'error': message
        }
        self._transport.sendto(dumps(error_data), addr)

    def join_game(self, data, addr):
        game = self.get_game(game_id=data.get('game_id'))
        player = game.add_player(addr)
        game.send_message(
            player,
            {'action': 'joined', 'snake': player.snake_packet()}
        )
        if game.can_start():
            self.queue = None
            game.start_game()

    def datagram_received(self, data, addr):
        data = parse_packet(data)
        action = data.get('action')
        if action == 'join':
            self.join_game(data, addr)
            return
        game_id = data.get('game_id')
        game = self.get_game(game_id=game_id)
        if game is None:
            self.send_error(addr, f"No such game exists for id `{game_id}`")
            return
        if game.is_running():
            game.process_action(action, data)
            return

    def generate_id(self):
        return uuid4().hex.upper()

    def get_game(self, *, game_id=None):
        if game_id is not None:
            return self.games.get(game_id)
        if self.queue is not None:
            return self.queue
        game_id = self.generate_id()
        self.queue = game = Game(game_id, self._transport, self.loop)
        self.games[game_id] = game
        return game


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server = loop.create_datagram_endpoint(
        lambda: Server(loop),
        local_addr=('0.0.0.0', 9999)
    )
    transport, protocol = loop.run_until_complete(server)
    loop.run_forever()
    transport.close()
    loop.close()
