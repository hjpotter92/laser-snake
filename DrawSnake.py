#!/usr/bin/env python

import Snake
from pygame.locals import *
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (190, 190, 190)
SIZE = (1024, 576)

head = [200, 50]
tail = [50, 50]

class window:
	corners = list()
	def __init__(self, snake = Snake.Snake() ):
		self.snake = snake
		self.clock = pygame.time.Clock()
		if not self.clock:
			print 'warning! clock disabled'
		self.font = pygame.font
		if not self.font:
			print 'warning! fonts disabled'
		self.screen = pygame.display
		if not self.screen:
			print 'warning! screen disabled'
		self.sound = pygame.mixer
		if not self.sound:
			print 'warning! sound disabled'
		pygame.init()
		self.s = self.screen.set_mode(SIZE)
		self.screen.set_caption( 'Laser Snake' )
		pygame.mouse.set_visible(0)

	def update_screen(self):
		while True:
			self.clock.tick(30)
			self.s.fill(WHITE)
			self.screen.update()
			pygame.draw.aalines(self.s, RED, False, self.snake.points, 15)
			self.snake.updateSnake()
			
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit(0)
				elif event.type == KEYDOWN:
					if event.key == K_UP:
						if self.snake.head_direction != [0, 1] and self.snake.head_direction != [0, -1]:
							self.snake.head_direction = [0, -1]
							
					elif event.key == K_DOWN:
						if self.snake.head_direction != [0, -1] and self.snake.head_direction != [0, 1]:
							self.snake.head_direction = [0, 1]
							
					elif event.key == K_LEFT:
						if self.snake.head_direction != [-1, 0] and self.snake.head_direction != [1, 0]:
							self.snake.head_direction = [-1, 0]

					elif event.key == K_RIGHT:
						if self.snake.head_direction != [1, 0] and self.snake.head_direction != [-1, 0]:
							self.snake.head_direction = [1, 0]
						
					elif event.key == K_ESCAPE:sys.exit(0)
			pygame.display.flip()

	def game_end(self):
		pass
	def game_running(self):
		pass

def main():
	w_obj = window()
	w_obj.update_screen()
              
if __name__ == "__main__":
    main()

