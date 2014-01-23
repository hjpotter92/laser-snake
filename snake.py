from ordinates import *

class Snake:
    head = Co_ordinates()
    tail = Co_ordinates()
    corners = list()
    def __init__( self, h, t, d ):
        self.head = h
        self.tail = t
        self.corners.append( [t, d] )
    def __insert_corner__( self, crn, d ):
        self.corners.append( [crn, d] )
