class Point:
    def __init__( self, x = 0, y = 0 ):
        self.x = x
        self.y = y
        self.__direction = {
	    	'up': { 'x': 0, 'y': -1 },
	    	'down': { 'x': 0, 'y': 1 }
	    }

    def getDirection( self, s ):
    	return self.__direction[s]

    def add(self, p):
    	return Point( self.x + p['x'], self.y + p['y'] )
