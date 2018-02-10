from math import log10
from random import choice, randint

import pygame

from pygame.locals import *

from enums import Colours, Direction
from food import Food
from snake import Snake
from vector import Vector, random_vector

GAME_FPS = 30
GAME_WINDOW = GAME_WIDTH, GAME_HEIGHT = 0, 0
GAME_FULLSCREEN = True

BLOCK_SIZE = 16
WORLD_SIZE = Vector((30, 30))

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


class Game:
    """
    The layer for handling the main game window and its individual elements.

    """
    title = "Laser Snake"

    def __init__(self):
        self.block_size = BLOCK_SIZE
        self.window = pygame.display.set_mode(GAME_WINDOW, GAME_FULLSCREEN)
        self.screen = pygame.Surface(WORLD_SIZE * BLOCK_SIZE)
        self.clock = pygame.time.Clock()
        self.world = pygame.Rect((0, 0), WORLD_SIZE)
        self.boundary = (
            self.world.topleft,
            self.world.bottomright - Direction.BOTTOM_RIGHT.value
        )
        self.font = pygame.font.Font(
            pygame.font.match_font('helvetica,tahoma,arial'),
            32
        )
        pygame.display.set_caption(self.title)
        pygame.mouse.set_visible(False)
        self.reset()

    def reset(self):
        self.running = True
        self.next_direction = Direction.RANDOM()
        starting = random_vector(*self.boundary)
        self.snake = Snake(
            starting,
            self.next_direction.value,
            length=5,
            color=Colours.RANDOM()
        )
        self.foods = set()
        self.generate_food()

    def generate_food(self):
        position = random_vector(
            *self.boundary,
            exceptions=self.snake
        )
        rand = randint(2, 9999)
        score = int(3 / log10(rand)) + 1
        self.foods.add(Food(position, score, Colours.RANDOM()))

    def check_exit(self, event):
        """Check if the user exited"""
        if (event.type == pygame.QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            self.running = False
            return True

    def key_input(self, event):
        if event.key in KEY_DIRECTION:
            self.next_direction = KEY_DIRECTION[event.key]
        elif event.key in (K_SPACE, K_r):
            self.reset()

    def cleanup(self):
        pygame.quit()

    def quit(self):
        pygame.quit()

    def block(self, position):
        return pygame.Rect(
            position * self.block_size,
            Direction.BOTTOM_RIGHT.value * self.block_size
        )

    def draw_text(self, text, position):
        self.window.blit(
            self.font.render(text, True, Colours.WHITE.value),
            position
        )

    def render(self):
        self.window.fill(Colours.BACKGROUND.value)
        self.screen.fill(Colours.WHITE.value)
        for segment in self.snake:
            pygame.draw.ellipse(
                self.screen,
                self.snake.get_color(),
                self.block(segment)
            )
        for food in self.foods:
            pygame.draw.rect(
                self.screen,
                food.get_color(),
                self.block(food.get_position())
            )
        self.window.blit(self.screen, self.window.get_rect(x=80, y=40))
        self.draw_text(
            "Score: {0:n}. Speed: {1:02.2f}".format(
                self.snake.get_score(),
                self.snake.get_speed()
            ),
            (80, 600)
        )

    def update(self, δt):
        self.snake.update(δt, self.next_direction.value)
        head = self.snake.head()
        for food in self.foods:
            if food.get_position() == head:
                self.foods.remove(food)
                self.snake.grow(food.get_score())
                self.generate_food()
        if self.snake.suicide():
            self.next_direction = Direction.NULL
            self.running = False
        if not self.world.collidepoint(head):
            self.snake.loop(*self.boundary)

    def run(self):
        while True:
            δt = self.clock.tick(GAME_FPS) / 1000.0
            pygame.event.pump()
            for event in pygame.event.get():
                if self.check_exit(event):
                    return
                if event.type == KEYUP:
                    self.key_input(event)
            if self.running is True:
                self.update(δt)
                self.render()
            pygame.display.flip()
        self.cleanup()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    game.quit()
