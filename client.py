import socket, json
from player import Player

class Client:
	def __init__( self, name, ip, port ):
		self.player = Player( name )
		self.socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.server = ( ip, port )
		self.packet_size = 1024
 
	def sendJoinRequest( self ):
		join_header = {
			'cmd': 'JOIN',
			'info': {
				'name': self.player.getNick()
			}
		}
		self.socket.sendto( json.dumps(join_header), self.server )
		data_receive = self.socket.recv( self.packet_size )
		reply = json.loads( data_receive )
		self.player.setPlayerId( reply['id'] )

	def sendReadyRequest( self ):
		ready_header = {
			'cmd': 'READY',
			'info': {}
		}
		self.socket.sendto( json.dumps(ready_header), self.server )
		data_receieve = self.socket.recv( self.packet_size )
		reply = json.loads( data_receive )
		print reply

	def sendStartRequest( self ):
		start_game_header = {
			'cmd': 'START',
			'info': {}
		}
		self.socket.sendto( json.dumps(ready_header), self.server )
		data_receieve = self.socket.recv( self.packet_size )
		reply = json.loads( data_receive )
		print reply

	def sendQuitRequest( self ):
		quit_header = {
			'cmd': 'QUIT',
			'info': {}
		}
		self.socket.sendto( json.dumps(ready_header), self.server )
		data_receieve = self.socket.recv( self.packet_size )
		reply = json.loads( data_receive )
		print reply

	def sendSnakeDataRequest( self ):
		snake_header = {
			'cmd': 'SNAKEDATA',
			'info': self.constructor
		}
		self.socket.sendto( json.dumps(ready_header), self.server )
		data_receieve = self.socket.recv( self.packet_size )
		reply = json.loads( data_receive )
		print reply

	def receiveData( self ):
		while True:
			rcvd = self.socket.recv( 1024 )
			print rcvd

if __name__ == "__main__":
	name = raw_input( "Please enter your nickname: " )
	ip = raw_input( "Enter server address: " )
	port = raw_input( "Enter server port: " )
	cl = Client( name, ip, int(port) )
	cl.sendJoinRequest()
	choice = raw_input ( "Are you ready? ")
	if 'yes' in choice.lower():
		cl.sendReadyRequest()
	
	

