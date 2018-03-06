import logging

from math import log10
from random import choice, randint

import pygame

from pygame.locals import *
from pygame.draw import ellipse as pyellipse, rect as pyrect, arc as pyarc

from enums import Colors, Direction
from food import Food
from snake import Snake
from vector import Vector, random_vector

GAME_FPS = 60
GAME_WINDOW = GAME_WIDTH, GAME_HEIGHT = 1280, 720
GAME_FULLSCREEN = False

WORLD_SIZE = Vector((16, 16))

KEY_DIRECTION = {
    K_w: Direction.UP,
    K_UP: Direction.UP,
    K_a: Direction.LEFT,
    K_LEFT: Direction.LEFT,
    K_s: Direction.DOWN,
    K_DOWN: Direction.DOWN,
    K_d: Direction.RIGHT,
    K_RIGHT: Direction.RIGHT,
}

FORMAT = '%(asctime)-15s [%(levelname)s] (%(name)s) %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('laser-snake.client.game')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('client.log'))


class SnakeGame:
    """
    The layer for handling the main game window and its individual elements.

    """
    title = "Laser Snake - "

    def __init__(self, game_id=None, *args, **kwds):
        self.client = kwds.get('client')
        self.game_id = game_id
        self.snake = kwds.get('snake')
        self.player_id = kwds.get('player_id')
        self.running = False
        self.foods = None

    def display(self, world_size):
        pygame.init()
        world_size = Vector(world_size) if world_size else WORLD_SIZE
        self.block_size = 480 // world_size[0]
        self.window = pygame.display.set_mode(GAME_WINDOW, GAME_FULLSCREEN)
        self.screen = pygame.Surface(world_size * self.block_size)
        self.clock = pygame.time.Clock()
        self.world = pygame.Rect((0, 0), world_size)
        self.font = pygame.font.Font(
            pygame.font.match_font('helvetica,tahoma,arial'),
            32
        )
        pygame.display.set_caption(f"{self.title}{self.game_id}")
        self.running = True

    def parse_snakes(self, snakes):
        # logger.critical(snakes)
        self.others = []
        for snake in snakes:
            player = snake.get('player')
            if player.get('id') == self.player_id:
                self.snake = snake
            else:
                self.others.append(snake)

    def check_exit(self, event):
        """Check if the user exited"""
        if (event.type == pygame.QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            self.running = False
            return True

    def key_input(self, event):
        if event.key in KEY_DIRECTION:
            self.next_direction = KEY_DIRECTION[event.key]
            self.client.send_message({
                'action': 'move',
                'head': self.snake.get('head'),
                'direction': self.next_direction.name
            })

    def cleanup(self):
        pygame.quit()

    def block(self, position):
        return pygame.Rect(
            Vector(position) * self.block_size,
            Direction.BOTTOM_RIGHT.value * self.block_size
        )

    def draw_text(self, text, position):
        self.window.blit(
            self.font.render(text, True, Colors.WHITE.value),
            position
        )

    def draw_snake(self, snake):
        head = snake.get('head')
        player = snake.get('player')
        color = Colors['BLUE' if player.get('id') == self.player_id else 'RED']
        pyellipse(
            self.screen,
            color.value,
            self.block(head)
        )
        for segment in snake.get('segments'):
            pyarc(
                self.screen,
                color.value,
                self.block(segment), 0, 360,
                self.block_size//4
            )

    def over(self):
        pygame.display.set_caption(f"{self.title}{self.game_id} - Game Over")

    def render(self):
        self.window.fill(Colors.BACKGROUND.value)
        self.screen.fill(Colors.WHITE.value)
        self.draw_snake(self.snake)
        for snake in self.others:
            self.draw_snake(snake)
        for food in self.foods:
            pyrect(
                self.screen,
                Colors.GREEN.value,
                self.block(food.get('position')),
                self.block_size // (4 * food.get('score'))
            )
        self.window.blit(self.screen, self.window.get_rect(x=80, y=40))
        self.draw_text(
            "Score: {0:n}".format(
                len(self.snake.get('segments'))
            ),
            (80, 600)
        )

    def run(self, **kwds):
        self.display(kwds.get('world_size'))
        self.parse_snakes(kwds.get('snakes'))
        logger.info("display started")
        while True:
            δt = self.clock.tick(GAME_FPS) / 1000.0
            pygame.event.pump()
            for event in pygame.event.get():
                if self.check_exit(event):
                    return
                if event.type == KEYUP:
                    self.key_input(event)
            if self.running is True:
                self.render()
            pygame.display.flip()
        self.cleanup()

    quit = cleanup


if __name__ == "__main__":
    pygame.init()
    game = SnakeGame()
    game.run()
    game.quit()
