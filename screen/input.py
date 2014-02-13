from pygame.locals import *
from pygame import font as pyfont, event as pyevent, display as pydisplay
from sys import exit

class Box:
	def __init__( self, screen, message, position, allowed_keys = [], background = (255, 255, 255), text = (255, 0, 0) ):
		pyfont.init()
		self.screen = screen
		self.message = message
		self.position = position
		if allowed_keys:
			self.allowed_keys = allowed_keys
		self.colours = {
			'screen': background,
			'text': text
		}
		self.font = pyfont.Font( None, 36 )

	def display( self, message ):
		self.screen.fill( self.colours['screen'] )
		if len( message ) > 0:
			text = self.font.render( message, 1, self.colours['text'] )
			self.screen.blit( text, self.position )
		pydisplay.flip()

	def run( self ):
		return_string = ""
		self.display( self.message )
		running = True
		while running:
			for event in pyevent.get():
				if event.type == QUIT:
					exit( 0 )
				elif event.type == KEYDOWN:
					key_code, key_unicode = event.key, event.unicode
					if key_code == K_ESCAPE:
						exit( 0 )
					if key_code == K_RETURN or key_code == K_KP_ENTER:
						running = False
						break
					elif key_code == K_BACKSPACE:
						return_string = return_string[:-1]
					elif key_code in self.allowed_keys:
						return_string += key_unicode
				self.display( self.message + " " + return_string )
		return return_string
