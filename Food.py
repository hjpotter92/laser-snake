from point import Point
from random import randint

class Food:
	def __init__( self, radius = 5, board_size = (1024, 576), max_food = 5 ):
		self.radius = radius
		self.board_size = board_size
		self.foods = []
		self.max_food = max_food

	def eatFood( self, point ):
		self.foods = filter( lambda food: abs(food[0] - point) >= food[1], self.foods )
		# print self.foods

	def genFood( self ):
		if self.max_food <= len(self.foods):
			pass
		else:
			x = randint(self.radius, self.board_size[0] - self.radius)
			y = randint(self.radius, self.board_size[1] - self.radius)
			self.foods.append( (Point( x, y ), self.radius) )

	def getFood( self ):
		return self.foods
