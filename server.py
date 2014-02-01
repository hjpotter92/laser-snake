import select, socket, sys, random, json

colours = [
	(19, 225, 30),
	(41, 2, 245),
	(251, 240, 32),
	(255, 255, 255),
	(0, 0, 0),
	(255, 0, 0)
]
def getColour():
	return colours[ random.randrange(0, len(colours)) ]

class server:
	def __init__( self, host, port ):
		self.listener = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.address = self.host, self.port = host, port
		self.listener.bind( self.address )
		self.reading = [ self.listener ]
		self.writing = []
		self.clients = {}

	def run( self ):
		try:
			while True:
				r, w, x = select.select( self.reading, self.writing, [], 0 )
				for f in r:
					data, addr = f.recvfrom( 32 )
					print data
					if addr not in self.clients:
						self.clients[addr] = data
				for t in self.clients:
					self.listener.sendto( json.dumps(getColour()), t )
		except socket.error, e:
			print e

if __name__ == "__main__":
	s = server( '', 1992 )
	s.run()
