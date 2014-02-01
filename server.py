import select, socket, sys

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
				# r, w, x = select.select( self.reading, self.writing, [], 2 )
				data, addr = self.listener.recvfrom( 32 )
				print data
				if addr not in self.clients:
					self.clients[addr] = data
		except socket.error, e:
			print e

if __name__ == "__main__":
	s = server( 'localhost', 1992 )
	s.run()
