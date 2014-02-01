import socket, select, pygame, pygame.locals, random, json

class client:
	def __init__( self, host, port ):
		self.server = self.servehost, self.serveport = host, port
		self.client = self.address, self.port = "localhost", random.randrange( 8000, 9000 )
		self.connection = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.connection.setblocking( 0 )
		self.connection.bind( self.client )
		self.readers = [ self.connection ]
		self.writers = []
		self.launchPygame( 600, 800 )

	def launchPygame( self, height, width ):
		self.screen = pygame.display.set_mode( (width, height) )
		pygame.event.set_allowed( None )
		pygame.event.set_allowed( [pygame.locals.QUIT, pygame.locals.KEYDOWN] )
		pygame.display.flip()

	def run( self ):
		flag = True
		clock = pygame.time.Clock()
		fps = 30
		try:
			self.connection.sendto( "JOIN", self.server )
			while flag:
				clock.tick( fps )
				r, w, e = select.select( self.readers, self.writers, [], 0 )
				for f in r:
					if f is self.connection:
						data, addr = f.recvfrom( 32 )
						print data
						new_colour = json.loads( data )
						self.screen.fill( new_colour )

				for event in pygame.event.get():
					if event.type in [ pygame.QUIT, pygame.locals.QUIT ]:
						flag = False
						break
					elif event.type == pygame.locals.KEYDOWN:
						if event.key == pygame.locals.K_ESCAPE:
							flag = False
							break
						pygame.event.clear( pygame.locals.KEYDOWN )
				pygame.display.update()
		except socket.error, e:
			print e
		finally:
			self.connection.sendto( "LEAVE", self.server )

if __name__ == "__main__":
	c = client( '', 1992 )
	c.run()
