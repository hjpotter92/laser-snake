#!/usr/bin/env python

from point import Point
from food import Food

class Snake:
	def __init__ ( self, food = Food(), board_size = Point(1024, 576), points = [Point(50, 50), Point(200, 50)], head_direction = Point(1, 0), meta = {} ):
		self.head_direction = head_direction
		self.points = points
		self.meta = meta
		self.food = food
		self.board_size = board_size

	def getFood( self ):
		return self.food.getFood()

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
		if dot == 0: self.points.append(new_head)
		else: self.setHead(new_head)
		if self.isPseudo(new_head): self.points += self.correspondingPseudo(new_head)

	def updateTail ( self ):
		tail_direction = self.getDirection (self.getTail(), self.points[1])
		new_tail = self.getTail() + tail_direction
		if new_tail == self.points[1]:
			self.points = self.points[1:]
		self.setTail(new_tail)
		if self.isPseudo(new_tail):
			self.points = self.points[1:]

	def isPseudo( self, p ):
		if p.y == -1 or p.x == -1 or p.x == self.board_size.x or p.y == self.board_size.y: return True
		else: return False

	def correspondingPseudo( self, p ):
		if p.y == -1: return [Point(p.x, self.board_size.y), Point(p.x, self.board_size.y - 1)]
		if p.x == -1: return [Point(self.board_size.x, p.y), Point(self.board_size.x -1, p.y)]
		if p.y == self.board_size.y: return [Point(p.x, -1), Point(p.x, 0)]
		if p.x == self.board_size.x: return [Point(-1, p.y), Point(0, p.y)]

	def sections( self ):
		secs = []
		i = 0
		l = len(self.points)
		while i < l:
			s = [self.points[i]]
			i = i + 1
			while(i < l and not self.isPseudo(self.points[i])):
				s.append(self.points[i])
				i = i + 1
			if i < l:
				s.append(self.points[i])
				i = i + 1
			secs.append(s)
		return secs

	def updateSnake( self ):
		self.updateHead()
		self.updateTail()
		self.food.eatFood(self.getHead())
		self.food.genFood()
