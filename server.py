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
		while True:
			try:
				data, addr = self.listener.recvfrom( 1024 )
				print data
			except socket.error, e:
				print e

if __name__ == "__main__":
	s = server( 'localhost', 1992 )
	s.run()
