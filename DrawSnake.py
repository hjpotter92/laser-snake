#!/usr/bin/env python

import Snake
class window:
	corners = list()
	def __init__(self, snake):
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

	def update_screen(self, list_snakes = []):
		directions = { 'UP': 0, 'RIGHT': 1, 'DOWN': 2, 'LEFT': 3, 'OPP_UP': 2, 'OPP_RIGHT': 3, 'OPP_DOWN': 0, 'OPP_LEFT': 1 }
		while True:
			self.clock.tick(30)
			self.s.fill(WHITE)
			self.screen.update()
			pygame.draw.aalines(self.s, RED, False, self.points, 15)

			self.snake.updateSnake()

			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit(0)
				elif event.type == KEYDOWN:
					if event.key == K_UP:
						if self.head_dir != directions['OPP_UP'] and self.head_dir != directions['UP']:
							self.head_dir = directions['UP']
							self.points, self.tail_dir = self.update_points(self.points, self.head_dir, self.tail_dir)

					elif event.key == K_DOWN:
						if self.head_dir != directions['OPP_DOWN'] and self.head_dir != directions['DOWN']:
							self.head_dir = directions['DOWN']
							self.points, self.tail_dir = self.update_points(self.points, self.head_dir, self.tail_dir)

					elif event.key == K_LEFT:
						if self.head_dir != directions['OPP_LEFT'] and self.head_dir != directions['LEFT']:
							self.head_dir = directions['LEFT']
							self.points, self.tail_dir = self.update_points(self.points, self.head_dir, self.tail_dir)

					elif event.key == K_RIGHT:
						if self.head_dir != directions['OPP_RIGHT'] and self.head_dir != directions['RIGHT']:
							self.head_dir = directions['RIGHT']
							self.points, self.tail_dir = self.update_points(self.points, self.head_dir, self.tail_dir)
						
					elif event.key == K_ESCAPE:sys.exit(0)
					print 'tail direction: ' + str(self.tail_dir)
					print ( self.points )
			
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

