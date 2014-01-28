#!/usr/bin/env python

import pygame, random, sys
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

class Snake:
	def __init__ ( self, points = [[0, 0],[10, 10]], head_direction = [1, 0], meta = {} ):
		self.head_direction = head_direction
		self.points = points
		self.meta = meta
	
	def addPoint ( self, p1, p2 ):
		return [p1[0] + p2[0], p1[1] + p2[1]]
	def multPoint( self, p1, x ):
		return [p1[0]*x, p1[1]*x]
	def distPoint( self, p ):
		return ( p[0]*p[0] + p[1]*p[1] ) ** (0.5)
	def slope( self, p1, p2 ):
		sub = self.addPoint( p1, self.multPoint ( p2, -1 ) ) 
		if sub == [0, 0]:
			print "Slope not defined ", p1, p2
			return 999999
		return self.multPoint( sub, 1/(self.distPoint(sub)) )  

	def getTailDirection( self ):
		#return slope(self.points[0], self.points[1])
		if self.points[0][0] == self.points[1][0]:
			if self.points[0][1] > self.points[1][1]:
				return [0, -1]
			else:
				return [0, 1]
		if self.points[0][1] == self.points[1][1]:
			if self.points[0][0] > self.points[1][0]:
				return [-1, 0]
			else:
				return [1, 0]
		else:
			print "tail error - ", points[0], points[1]
		
	

	def updateSnake( self ):
		tail_direction = self.getTailDirection ()
		self.points[-1] = self.addPoint( self.points[-1], self.head_direction )
		self.points[0]  = self.addPoint( self.points[0], tail_direction )
		if self.points[0] == self.points[1]:
			self.points = self.points[1:]
