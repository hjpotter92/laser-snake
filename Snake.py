#!/usr/bin/env python

from Point import *
from Food import Food

class Snake:
	def __init__ ( self, food = Food(), board_size = (1024, 768), points = [Point(100, 50), Point(200, 50)], head_direction = Point(1, 0), meta = {} ):
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
		if direction * self.head_direction == 0:
			self.head_direction = direction
		
	def updateHead( self, speed ):
		new_head = self.getHead() + speed * self.head_direction
		dot = self.head_direction * (self.getHead() - self.points[-2])

		if dot == 0:
			self.points.append(new_head) 
		else:
			self.setHead(new_head)
		
	def updateTail ( self, speed ):
		tail_direction = self.getDirection (self.getTail(), self.points[1])
		new_tail = self.getTail() + speed * tail_direction

		self.setTail(new_tail)
		if self.points[0] == self.points[1]:
			self.points = self.points[1:]

	def updateSnake( self, speed = 1 ):
		self.updateHead(speed)
		self.updateTail(speed)
		self.food.eatFood(self.getHead())
		self.food.genFood()
