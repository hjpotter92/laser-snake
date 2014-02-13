import socket
from pygame.locals import *
from pygame import font as pyfont, event as pyevent, display as pydisplay
from player import Player
from connection import send, receive
from screen.input import Box
from config import server as server_configuration

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
				request, address = receive( self.listener )
				if request['cmd'] in self.handler:
					print '{} comamnd received from {}'.format( request['cmd'], address[0] )
					self.handler[ request['cmd'] ]( self, request, address )
				else:
					print request['cmd']
			except socket.error:
				pass

if __name__ == '__main__':
	screen = pydisplay.set_mode( (1024, 576) )
	pydisplay.set_caption( "Laser-Snake server: " + server_configuration['version'] )
	pyevent.set_allowed( None )
	pyevent.set_allowed( [QUIT, KEYDOWN] )
	port_keys = range( K_0, K_9 + 1 ) + range( K_KP0, K_KP9 + 1 )
	ip_keys = port_keys + [ K_PERIOD, K_KP_PERIOD ]
	ip_box = Box( screen, "Please enter the server IP address: ", (10, 100), ip_keys )
	port_box = Box( screen, "Please enter the port to start server (leave blank for default): ", (10, 100), port_keys )
	ip = ip_box.run()
	port = port_box.run()
	if len( ip ) == 0 or len( port ) == 0:
		ip, port = ip or server_configuration['ip'], int( port or server_configuration['port'] )
	serve = Server( ip, int(port) )
	serve.receive()
