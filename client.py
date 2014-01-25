import socket, cPickle as pickle
from player import Player

class Client:
	def __init__( self, name, ip, port ):
		self.player = Player( name )
		self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.server = ( ip, port )

	def sendName( self ):
		self.socket.sendto( pickle.dumps(self.player), self.server )

	def receiveData( self ):
		while True:
			rcvd = self.socket.recv( 1024 )
			print rcvd

if __name__ == "__main__":
	name = raw_input( "Please enter your nickname: " )
	ip = raw_input( "Enter server address: " )
	port = raw_input( "Enter server port: " )
	cl = Client( name, ip, int(port) )
	cl.sendName()
	cl.receiveData()
