import socket, json, cPickle as pickle
from player import Player

class Server:
	def __init__( self, host, port ):
		self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.socket.setblocking( False )
		self.socket.bind( (host, port) )
		# self.socket.listen( 4 )
		print "Established connection on {} over {}".format( host, port )
		self.list_users = {}

	def receive( self ):
		while True:
			try:
				data, addr = self.socket.recvfrom( 1024 )
				pl = pickle.loads( data )
				print '{} connected from {}'.format( pl.getNick(), addr[0] )
				self.socket.sendto( '{} users tracked.'.format(len( self.list_users )), addr )
				if addr not in self.list_users:
					self.list_users[addr] = data
			except socket.error:
				pass

if __name__ == "__main__":
	ip = raw_input( "Please enter the server IP address (this is shared with clients to connect): " )
	port = raw_input( "Please enter the port to start server (leave blank for default): " )
	if len( ip ) == 0 or len( port ) == 0:
		with open( 'config/server.json') as config:
			server_configuration = json.load( config )
			ip, port = server_configuration['ip'], int( server_configuration['port'] )
	srvr = Server( ip, int(port) )
	srvr.receive()
