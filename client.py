import pygame

from pygame.locals import *


class Snake:
    x = []
    y = []
    color = (255, 0, 0)
    length = 1
    speed = 0
    RADIUS = 2
    __direction = 0  # 0 = right, 1 = up, 2 = left, 3 = down

    def __init__(self, length=1, speed=1):
        self.length = length
        self.speed = speed
        self.x = [self.RADIUS * 30] * self.length
        self.y = [self.RADIUS * 30] * self.length
        self.updater = False

    def __str__(self):
        return f"({self.x}, {self.y})"

    def get_direction(self):
        return self.__direction

    def move_right(self):
        self.__direction = 0

    def move_up(self):
        self.__direction = 1

    def move_left(self):
        self.__direction = 2

    def move_down(self):
        self.__direction = 3

    def update(self):
        self.updater = not self.updater
        if not self.updater:
            return
        for _ in range(self.length - 1, 0, -1):
            self.x[_] = self.x[_ - 1]
            self.y[_] = self.y[_ - 1]
        MULTIPLIER = (self.speed - 1) * self.RADIUS * 2
        if self.get_direction() == 0:
            self.x[0] += MULTIPLIER
        if self.get_direction() == 1:
            self.y[0] -= MULTIPLIER
        if self.get_direction() == 2:
            self.x[0] -= MULTIPLIER
        if self.get_direction() == 3:
            self.y[0] += MULTIPLIER

    def draw(self, surface, shape):
        if self.x[0] > surface.get_width():
            self.x.insert(0, 0)
            self.y.insert(0, self.y[0])
        if self.x[0] < 0:
            self.x.insert(0, surface.get_width())
            self.y.insert(0, self.y[0])
        if self.y[0] > surface.get_height():
            self.y.insert(0, 0)
            self.x.insert(0, self.x[0])
        if self.y[0] < 0:
            self.y.insert(0, surface.get_height())
            self.x.insert(0, self.x[0])
        self.x = self.x[0:self.length]
        self.y = self.y[0:self.length]
        for x, y in zip(self.x, self.y):
            shape(
                surface,
                self.color,
                (x, y),
                self.RADIUS * 2
            )


class Game:
    size = wide, high = 800, 600
    title = "Laser Snake"

    def __init__(self):
        self._running = False
        pygame.init()
        self.snake = Snake(length=30, speed=3)

    def on_init(self):
        self._screen = pygame.display.set_mode(self.size)
        self._clock = pygame.time.Clock()
        pygame.display.set_caption(self.title)
        pygame.mouse.set_visible(0)
        self._running = True
        return True

    def check_exit(self):
        """Check if the user exited"""
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == KEYDOWN and event.key == K_ESCAPE)):
                self._running = False

    def cleanup(self):
        pygame.quit()

    def check_key(self, key):
        if key[K_RIGHT]:
            self.snake.move_right()
        if key[K_UP]:
            self.snake.move_up()
        if key[K_DOWN]:
            self.snake.move_down()
        if key[K_LEFT]:
            self.snake.move_left()

    def in_loop(self):
        self.snake.update()
        pygame.display.flip()

    def render(self):
        self._clock.tick(30)
        self._screen.fill((128, 255, 144))
        self.snake.draw(self._screen, pygame.draw.circle)

    def run(self):
        if self.on_init() is not True:
            self._running = False
        while self._running:
            self.render()
            pygame.event.pump()
            self.check_exit()
            keys = pygame.key.get_pressed()
            self.in_loop()
            self.check_key(keys)
        self.cleanup()


if __name__ == "__main__":
    s = Game()
    s.run()
