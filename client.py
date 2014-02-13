import socket
from pygame.locals import *
from pygame import font as pyfont, event as pyevent, display as pydisplay
from sys import exit
from player import Player
from connection import send, receive
from screen.input import Box
from config import game as game_configuration

class Client:
	packet_size = 1024

	def __init__( self, name, ip, port ):
		self.player = Player( name )
		self.connection = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.server = ( ip, port )

	def sendJoinRequest( self ):
		join_header = {
			'cmd': 'JOIN',
			'info': {
				'name': self.player.getNick()
			}
		}
		send( self.connection, join_header, self.server )
		reply, address = receive( self.connection, self.packet_size )
		self.player.setPlayerId( reply['self']['id'] )

	def sendReadyRequest( self ):
		ready_header = {
			'cmd': 'READY',
			'info': {
				'player_id': self.player.getPlayerId()
			}
		}
		send( self.connection, ready_header, self.server )
		reply, address = receive( self.connection, self.packet_size )
		print reply

	def sendStartRequest( self ):
		start_game_header = {
			'cmd': 'START',
			'info': {
				'player_id': self.player.getPlayerId()
			}
		}
		send( self.connection, start_game_header, self.server )
		reply, address = receive( self.connection, self.packet_size )
		print reply

	def sendQuitRequest( self ):
		quit_header = {
			'cmd': 'QUIT',
			'info': {
				'player_id': self.player.getPlayerId()
			}
		}
		send( self.connection, quit_header, self.server )
		reply, address = receive( self.connection, self.packet_size )
		print reply

	def sendSnakeDataRequest( self ):
		snake_header = {
			'cmd': 'SNAKEDATA',
			'info': {
				'player_id': self.player.getPlayerId(),
				'data': self.constructor
			}
		}
		send( self.connection, snake_header, self.server )
		reply, address = receive( self.connection, self.packet_size )
		print reply

	def receiveCountDownRequest( self ):
		data_receive = receive( self.connection, self.packet_size )

	def sendName( self ):
		send( self.connection, self.player.getNick(), self.server )

	def receiveData( self ):
		while True:
			data_receive = receive( self.connection, self.packet_size )
			print data_receive

if __name__ == "__main__":
	screen_size = ( game_configuration['screenW'], game_configuration['screenH'] )
	screen = pydisplay.set_mode( screen_size )
	pydisplay.set_caption( "Laser-Snake: " + game_configuration['version'] )
	pyevent.set_allowed( None )
	pyevent.set_allowed( [QUIT, KEYDOWN] )
	nick_keys, port_keys = range( K_LEFTPAREN, K_z + 1 ) + range( K_KP0, K_KP_PLUS + 1 ) + [ K_KP_EQUALS ], range( K_0, K_9 + 1 ) + range( K_KP0, K_KP9 + 1 )
	ip_keys = port_keys + [ K_PERIOD, K_KP_PERIOD ]
	nick_box = Box( screen, "Enter your nickname: ", (150, 100), nick_keys )
	ip_box = Box( screen, "Enter server IP: ", (150, 100), ip_keys )
	port_box = Box( screen, "Enter server port: ", (150, 100), port_keys )
	name = nick_box.run()
	ip = ip_box.run()
	port = port_box.run()
	if len( ip ) == 0 or len( port ) == 0:
		ip, port = ip or game_configuration['ip'], port or game_configuration['port']
	client = Client( name, ip, int(port) )
	client.sendJoinRequest()
	choice_box = Box( screen, "Are you ready? (yes/no) ", (150, 100), nick_keys )
	choice = choice_box.run()
	if 'yes' in choice.lower():
		client.sendReadyRequest()
	client.receiveCountDown()
