#!/usr/bin/env python

class Snake:
	def __init__ ( self, points = [[100, 50],[150, 50]], head_direction = [1, 0], meta = {} ):
		self.head_direction = head_direction
		self.points = points
		self.meta = meta
	
	def addPoint ( self, p1, p2 ):
		return [p1[0] + p2[0], p1[1] + p2[1]]

	def subPoint (self, p1, p2 ):
		return [p1[0] - p2[0], p1[1] - p2[1]]

	def multPoint( self, p1, x ):
		return [p1[0]*x, p1[1]*x]

	def distPoint( self, p ):
		return ( p[0]*p[0] + p[1]*p[1] ) ** (0.5)

	def dotProduct( self, p1, p2 ):
		return p1[0]*p2[0] + p1[1]*p2[1]

	def slope( self, p1, p2 ):
		sub = self.subPoint( p2, p1 ) 
		if sub == [0, 0]:
			print "Slope not defined ", p1, p2
			return 999999
		return self.multPoint( sub, 1/(self.distPoint(sub)) )  

	def getDirection( self, p1, p2 ):
		if p1[0] != p2[0] and p1[1] != p2[1]:
			print "direction error: ", self.points[0], self.points[1]
		s = self.slope(p1, p2)
		return [int(round(s[0])),int(round(s[1]))]

	def updateDirection( self, direction ):
		if self.dotProduct( direction, self.head_direction ) == 0:
			self.head_direction = direction
				
	def updateSnake( self ):
		tail_direction = self.getDirection (self.points[0], self.points[1])
		new_head = self.addPoint( self.points[-1], self.head_direction )
		new_tail = self.addPoint( self.points[0] , tail_direction)
		
		dot = self.dotProduct (self.head_direction, self.subPoint( self.points[-1], self.points[-2] ) )
		if dot == 0:
			self.points.append( new_head ) 
		else:
			self.points[-1] = new_head
			
		self.points[0] = new_tail
		if self.points[0] == self.points[1]:
			self.points = self.points[1:]

		
			



