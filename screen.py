import pygame
import random
import sys
from snake import *
from ordinates import *
from pygame.locals import *

clock = pygame.time.Clock()
screen = pygame.display
font = pygame.font
display = pygame.display

pygame.init()
s = screen.set_mode( (1024, 576) )
screen.set_caption( 'Laser Snake' )

def main():
    directions = {
        'UP': 0,
        'LEFT': 1,
        'DOWN': 2,
        'RIGHT': 3,
        0: 'UP',
        1: 'LEFT',
        2: 'DOWN',
        3: 'RIGHT'
    }
    while True:
        clock.tick(30)
        s.fill( (192,192,192) )
        display.update()
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit(0)
            elif e.type == KEYDOWN:
                if e.key == K_UP:
                    print( directions[directions['UP']] )
                elif e.key == K_DOWN:
                    print( directions[directions['DOWN']] )
                elif e.key == K_LEFT:
                    print( directions[directions['LEFT']] )
                elif e.key == K_RIGHT:
                    print( directions[directions['RIGHT']] )
                elif e.key == K_ESCAPE:
                    sys.exit(0)

if __name__ == "__main__":
    main()
