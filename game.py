from math import log10
from random import choice, randint

import pygame

from pygame.locals import *

from enums import Colours, Direction
from food import Food
from snake import Snake
from vector import Vector, random_vector

GAME_FPS = 30
GAME_WINDOW = GAME_WIDTH, GAME_HEIGHT = 1280, 720

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
        self.window = pygame.display.set_mode(GAME_WINDOW)
        self.screen = pygame.Surface(WORLD_SIZE * BLOCK_SIZE)
        self.clock = pygame.time.Clock()
        self.world = pygame.Rect((0, 0), WORLD_SIZE)
        self.boundary = (
            self.world.topleft,
            self.world.bottomright - Direction.BOTTOM_RIGHT.value
        )
        self.food = set()
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
        self.generate_food()

    def generate_food(self):
        position = random_vector(
            *self.boundary,
            exceptions=self.snake
        )
        rand = randint(1, 9999)
        score = int(3 / log10(rand)) + 1
        self.food.add(Food(position, score, Colours.RANDOM()))

    def check_exit(self, event):
        """Check if the user exited"""
        if (event.type == pygame.QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            self.running = False
            return True

    def key_input(self, event):
        if event.key in KEY_DIRECTION:
            self.next_direction = KEY_DIRECTION[event.key]

    def cleanup(self):
        pygame.quit()

    def block(self, position):
        return pygame.Rect(
            position * self.block_size,
            Direction.BOTTOM_RIGHT.value * self.block_size
        )

    def update(self, δt):
        self.snake.update(δt, self.next_direction.value)
        head = self.snake.head()
        for food in self.food:
            if food.get_position() == head:
                self.food.remove(food)
                self.snake.grow(food.get_score())
                self.generate_food()
        if self.snake.suicide():
            self.running = False
        if not self.world.collidepoint(head):
            self.snake.loop(*self.boundary)

    def render(self):
        # self.window.fill(Colours.BACKGROUND.value)
        self.screen.fill(Colours.BACKGROUND.value)
        for segment in self.snake:
            pygame.draw.ellipse(
                self.screen,
                self.snake.get_color(),
                self.block(segment)
            )
        for food in self.food:
            pygame.draw.rect(
                self.screen,
                food.get_color(),
                self.block(food.get_position())
            )
        self.window.blit(self.screen, self.window.get_rect(x=80, y=40))

    def run(self):
        while self.running:
            δt = self.clock.tick(GAME_FPS) / 1000.0
            self.render()
            pygame.event.pump()
            for event in pygame.event.get():
                if self.check_exit(event):
                    break
                if event.type == KEYUP:
                    self.key_input(event)
            self.update(δt)
            pygame.display.flip()
        self.cleanup()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
