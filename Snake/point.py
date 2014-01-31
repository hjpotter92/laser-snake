import math

class Point:
	def __init__( self, x = 0, y = 0 ):
		self.x = x
		self.y = y

	def __add__( self, other ):
		return Point( self.x + other.x, self.y + other.y )

	def __sub__( self, other ):
		return Point( self.x - other.x, self.y - other.y )

	def __div__( self, other ):
		return Point( self.x / other, self.y / other )

	def __mul__( self, other ):
		return self.x * other.x + self.y * other.y

	def __rmul__( self, other ):
		return Point( other * self.x, other * self.y )

	def __abs__( self ):
		return math.sqrt( self.x * self.x + self.y * self.y)

	def __str__( self ):
		return '({}, {})'.format( self.x, self.y )

	def __repr__( self ):
		return '({}, {})'.format( self.x, self.y )

	def __eq__( self, other ):
		return ( self.x == other.x ) and ( self.y == other.y )

	def slope ( self, other ):
		return ( other - self ) / abs( other - self )

	def toList( self ):
		return [ self.x, self.y ]
