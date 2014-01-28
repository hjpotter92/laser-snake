#!/usr/bin/env python

import sys
import pygame
import Snake
from Point import *
from pygame.locals import *



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (190, 190, 190)
SIZE = (1024, 576)

head = [200, 50]
tail = [50, 50]
fps = 50
speed = 5
food_radius = 5

class window:
	corners = list()
	def __init__(self, snake = Snake.Snake()):
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

	key_handler = {
		K_UP: Point(0, -1),
		K_DOWN: Point(0, 1),
		K_LEFT: Point(-1, 0),
		K_RIGHT: Point(1, 0)
	}

	def updateScreen(self):
		while True:
			self.clock.tick(fps)
			self.s.fill(WHITE)
			self.screen.update()
			self.snake.updateSnake(speed)
			
			for food in self.snake.food.foods:
				pygame.draw.circle(self.s, GREEN, toList(food[0]), food[1], 0)				
			pygame.draw.aalines(self.s, BLUE, False, map( toList, self.snake.points ), 15)

			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit(0)
				if event.type == KEYDOWN:					
					if event.key in self.key_handler:
						self.snake.updateDirection( self.key_handler[event.key] )
					elif event.key == K_ESCAPE:
						sys.exit(0)
			pygame.display.flip()

def main():
	w_obj = window()
	w_obj.updateScreen()
              
if __name__ == "__main__":
    main()

