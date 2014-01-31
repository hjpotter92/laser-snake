import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import sys

def get_key():
	while 1:
		event = pygame.event.poll()
		if event.type == KEYDOWN:
			return event.key
		else: pass

def display_box(screen, message):
	fontobject = pygame.font.Font(None,24)
	screen.fill((138, 138, 138))
	if len(message) != 0:
		f = fontobject.render(message, 1, (255, 255, 255))
		dest = ( int((screen.get_width() - f.get_width()) / 2)  , int((screen.get_height() - f.get_height()) / 2))
		screen.blit(f, dest)

	pygame.display.flip()

def ask(screen, question):
	pygame.font.init()
	current_string = []
	display_box(screen, question + string.join(current_string,""))
	while 1:
		inkey = get_key()
		if inkey == K_ESCAPE:
			sys.exit(0)
		elif inkey == K_BACKSPACE:
			current_string = current_string[0:-1]
		elif inkey == K_RETURN:
			break
		elif inkey == K_MINUS:
			current_string.append("_")
		elif inkey <= 127:
			current_string.append(chr(inkey))
		display_box(screen, question + string.join(current_string,""))
	return string.join(current_string,"")

def main():
	screen = pygame.display.set_mode((600,300))
	print ask(screen, "server address - ") + " was entered"
	print ask(screen, "port - ") + " was entered"

if __name__ == '__main__': main()
