import socket
from player import Player
from connection import send, receive

class Server:
	def __init__( self, host, port ):
		self.listener = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.listener.bind( (host, port) )
		print "Established connection on {} over port {}".format( host, port )
		self.reader = [ self.listener ]
		self.players = {}

	def sendData( self ):
		for address in self.players:
			self.players[address]['playing'] = True
			send( self.listener, reply, address )

	def receiveJoinRequest( self, request, address ):
		self.players[address] = {
			'id': len(self.players) + 1,
			'name': request['info']['name'],
			'ready': False,
			'playing' : False
		}
		reply = {
			'self': {
				'id': self.players[address]['id']
			},
			'other_players': ""
		}
		send( self.listener, reply, address )
		self.players[address]['player'] = Player( self.players[address]['name'], self.players[address]['id'] )

	def receiveReadyRequest( self, request, address ):
		self.players[address]['ready'] = True
		print self.players[address]['name']+ ' is ' + ' READY'

	def receiveStartRequest( self, request, address ):
 		for addr in self.players:
 			if not self.players[addr]['ready']:
 				reply = {
 					'response': 'ERROR',
 					'info': 'All the players are not yet ready to play.'
 				}
 				send( self.listener, reply, address )
 				return False
		if address in self.players and self.players[address]['id'] == 1:
			time.sleep(10)
			self.sendData()
		else:
			reply = {
				'response': 'ERROR',
				'info': 'Only the player who joined first can start the game.'
			}
 			send( self.listener, reply, address )

	def receiveSnakeDataReuqest( self, request, address ):
		self.players[address][snake] = request['info']

	def receiveQuitRequest( self, request, address ):
		self.players[address]['playing'] = False

	handler = {
		'JOIN': receiveJoinRequest,
		'READY': receiveReadyRequest,
		'START': receiveStartRequest,
		'SNAKEDATA': receiveSnakeDataReuqest,
		'QUIT': receiveQuitRequest
	}

	def receive( self ):
		while True:
			try:
				receive_data, address = receive( self.listener )
				if request['cmd'] in self.handler:
					print '{} comamnd received from {}'.format( request['cmd'], address[0] )
					self.handler[ request['cmd'] ]( self, request, address )
				else:
					print request['cmd']
			except socket.error:
				pass

if __name__ == '__main__':
	ip = raw_input( "Please enter the server IP address (this is shared with clients to connect): " )
	port = raw_input( "Please enter the port to start server (leave blank for default): " )
	if len( ip ) == 0 or len( port ) == 0:
		with open( 'config/server.json') as config:
			server_configuration = json.load( config )
			ip, port = ip or server_configuration['ip'], int( port or server_configuration['port'] )
	serve = Server( ip, int(port) )
	serve.receive()
