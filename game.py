from math import log10
from random import choice, randint

import pygame

from pygame.locals import *
from pygame.draw import ellipse as pyellipse, rect as pyrect, arc as pyarc

from enums import Colors, Direction
from food import Food
from snake import Snake
from vector import Vector, random_vector

GAME_FPS = 30
GAME_WINDOW = GAME_WIDTH, GAME_HEIGHT = 1280, 720
GAME_FULLSCREEN = False

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


class SnakeGame:
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
            color=Colors.BLUE
        )
        self.snakes = [
            Snake(
                random_vector(*self.boundary),
                Direction.RANDOM().value,
                color=Colors.RED
            )
            for i in range(3)
        ]
        self.foods = set()
        self.generate_food()

    def generate_food(self):
        position = random_vector(
            *self.boundary,
            exceptions=self.snake
        )
        rand = randint(2, 9999)
        score = int(3 / log10(rand)) + 1
        self.foods.add(Food(position, score, Colors.GREEN))

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
            self.font.render(text, True, Colors.WHITE.value),
            position
        )

    def draw_snake(self, snake):
        snake_head = snake.head()
        for segment in snake:
            if snake_head is segment:
                pyellipse(
                    self.screen,
                    snake.get_color(),
                    self.block(segment)
                )
            else:
                pyarc(
                    self.screen,
                    snake.get_color(),
                    self.block(segment), 0, 360,
                    self.block_size//4
                )

    def render(self):
        self.window.fill(Colors.BACKGROUND.value)
        self.screen.fill(Colors.WHITE.value)
        self.draw_snake(self.snake)
        for snake in self.snakes:
            self.draw_snake(snake)
        for food in self.foods:
            pyrect(
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
        for snake in self.snakes:
            snake.update(δt, Direction.RANDOM().value)
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
        for snake in self.snakes:
            head = snake.head()
            if not self.world.collidepoint(head):
                snake.loop(*self.boundary)

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
    game = SnakeGame()
    game.run()
    game.quit()
