import pygame
from points import *

class Snake:
    def __init__( self, h, t, d, meta ):
        self.head = h
        self.tail = t
        self.d = d
        self.corners = [t, h]
        self.meta = meta

    def updateSnake( self, save_head = False ):
    	self.head = self.head.add( self.head.getDirection(self.d) )
    	if save_head == True:
    		self.corners.append( self.head )
    	else:
    		self.corners[-1] = self.head

    def drawSnake( self, screen ):
    	pygame.draw.lines( screen, self.meta['colour'], False, [[p.x, p.y] for p in self.corners], 15 )
