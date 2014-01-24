import socket, json
from player import *

class Server:
	def __init__( self, host = "", port = 1992 ):
		self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.socket.setblocking( False )
		self.socket.bind( (host, port) )
		self.list_users = {}

	def receive( self ):
		while True:
			try:
				data, addr = self.socket.recvfrom( 1024 )
				self.socket.sendto( json.dumps(data.upper()), addr )
				if addr not in self.list_users:
					self.list_users[addr] = data
			except socket.error:
				pass

srvr = Server()

def receive():
	srvr.receive()

if __name__ == "__main__":
	receive()
