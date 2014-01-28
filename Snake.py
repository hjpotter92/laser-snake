#!/usr/bin/env python

from Point import *
from Food import Food

class Snake:
	def __init__ ( self, food = Food(), board_size = (1024, 576), points = [Point(50, 50), Point(200, 50)], head_direction = Point(1, 0), meta = {} ):
		self.head_direction = head_direction
		self.points = points
		self.meta = meta
		self.food = food

	def getHead ( self ):
		return self.points[-1]

	def getTail ( self ):
		return self.points[0]

	def setHead ( self, p ):
		self.points[-1] = p

	def setTail ( self, p ):
		self.points[0] = p

	def getDirection( self, p1, p2 ):
		s = p1.slope(p2)
		return Point( int(round(s.x)), int(round(s.y)) )

	def updateDirection( self, direction ):
		if direction * (self.getHead() - self.points[-2]) == 0:
			self.head_direction = direction


	def updateHead( self ):
		new_head = self.getHead() + self.head_direction
		dot = self.head_direction * (self.getHead() - self.points[-2])

		if dot == 0:
			self.points.append(new_head)
		else:
			self.setHead(new_head)

	def updateTail ( self ):
		tail_direction = self.getDirection (self.getTail(), self.points[1])
		new_tail = self.getTail() + tail_direction
		if new_tail == self.points[1]:
			self.points = self.points[1:]
		self.setTail(new_tail)

	def updateSnake( self ):
		self.updateHead()
		self.updateTail()
		self.food.eatFood(self.getHead())
		self.food.genFood()
