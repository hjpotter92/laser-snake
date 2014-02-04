import socket
from player import Player
from connection import send, receive

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
		reply = receive( self.connection )
		self.player.setPlayerId( reply['id'] )

	def sendReadyRequest( self ):
		ready_header = {
			'cmd': 'READY',
			'info': {
				'player_id': self.player.getPlayerId()
			}
		}
		send( self.connection, ready_header, self.server )
		reply = receive( self.connection )
		print reply

	def sendStartRequest( self ):
		start_game_header = {
			'cmd': 'START',
			'info': {
				'player_id': self.player.getPlayerId()
			}
		}
		send( self.connection, start_game_header, self.server )
		reply = receive( self.connection )
		print reply

	def sendQuitRequest( self ):
		quit_header = {
			'cmd': 'QUIT',
			'info': {
				'player_id': self.player.getPlayerId()
			}
		}
		send( self.connection, quit_header, self.server )
		reply = receive( self.connection )
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
		reply = receive( self.connection )
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
	name = raw_input( "Please enter your nickname: " )
	ip = raw_input( "Enter server address: " )
	port = raw_input( "Enter server port: " )
	cl = Client( name, ip, int(port) )
	cl.sendJoinRequest()
	choice = raw_input ( "Are you ready? (yes/no) ")
	if 'yes' in choice.lower():
		cl.sendReadyRequest()
	cl.receiveCountDown()
