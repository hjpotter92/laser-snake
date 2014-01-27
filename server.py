import socket, json
from player import Player

class Server:
	def __init__( self, host, port ):
		self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.socket.setblocking( False )
		self.socket.bind( (host, port) )
		# self.socket.listen( 4 )
		print "Established connection on {} over {}".format( host, port )
		self.players = {}

	def receiveJoinRequest( self, info, address ):
		if address not in self.players:
			self.players[address] = {
				'id': len(self.players) + 1,
				'name': info['name']
			}
		return self.players[address]['id']
		
	def receiveReadyRequest( self, info, address ):
		self.players[address]['ready'] = True
		print info, "READY"

	def receive( self ):
		while True:
			try:
				receive_data, address = self.socket.recvfrom( 1024 )
				request = json.loads( receive_data )
				if 'cmd' in request:
					if request['cmd'] == 'JOIN':
						reply = {
							'id': self.receiveJoinRequest( request['info'], address )
						}
						self.socket.sendto( json.dumps(reply), address )
					elif request['cmd'] == 'READY':
						self.receiveReadyRequest( request['info'], address )
					elif request['cmd'] == 'START':
						print "START"
					elif request['cmd'] == 'SNAKEDATA':
						print "DATA"
					elif request['cmd'] == 'QUIT':
						print "QUIT"
					else:
						self.receiveInvalidRequest( address )
		
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
