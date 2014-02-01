import socket, select, pygame, pygame.locals, random, json

colours = [
	(19, 225, 30),
	(41, 2, 245),
	(251, 240, 32),
	(255, 255, 255),
	(0, 0, 0),
	(255, 0, 0)
]

class client:
	def __init__( self, host, port ):
		self.server = self.servehost, self.serveport = host, port
		self.client = self.address, self.port = "localhost", random.randrange( 8000, 9000 )
		self.connection = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.connection.bind( self.client )
		self.readers = [ self.connection ]
		self.writers = []
		self.launchPygame( 600, 800, colours[2] )

	def launchPygame( self, height, width, colour ):
		self.screen = pygame.display.set_mode( (width, height) )
		self.screen.fill( colour )
		pygame.display.flip()

	def newColour( self ):
		return colours[ random.randrange(0, len(colours)) ]

	def run( self ):
		flag = True
		clock = pygame.time.Clock()
		fps = 30
		try:
			self.connection.sendto( "JOIN", self.server )
			while flag:
				clock.tick( fps )
				r, w, e = select.select( self.readers, self.writers, [], 4 )
				for f in r:
					if f is self.connection:
						data, addr = f.recvfrom( 1024 )
						print data

				for event in pygame.event.get():
					if event.type in [ pygame.QUIT, pygame.locals.QUIT ]:
						flag = False
						break
					elif event.type == pygame.locals.KEYDOWN:
						if event.key == pygame.locals.K_ESCAPE:
							flag = False
							break
						else:
							new_colour = self.newColour()
							self.screen.fill( new_colour )
							self.connection.sendto( json.dumps(new_colour), self.server )
						pygame.event.clear( pygame.locals.KEYDOWN )
				pygame.display.flip()
		except socket.error, e:
			print e
		finally:
			self.connection.sendto( "LEAVE", self.server )

if __name__ == "__main__":
	c = client( 'localhost', 1992 )
	c.run()
