#!/usr/bin/env python

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

	def sendData( self ):
		for address in self.players:
			self.socket.sendto( json.dumps(reply), address )

	def receiveJoinRequest( self, request, address ):
		self.players[address] = {
			'id': len(self.players) + 1,
			'name': request['info']['name'],
			'ready': False,
			'playing' : False
		}
		reply = self.players[address]
		self.socket.sendto( json.dumps(reply), address )
		
	def receiveReadyRequest( self, request, address ):
		self.players[address]['ready'] = True
		print self.players[address]['name']+ ' is ' + ' READY'

	def receiveStartRequest( self, request, address ):
		if address in self.players and self.players[address]['id'] == 1:
			time.sleep(10)
			self.sendData()			
		else:
			reply = 'Only the player who joined first can start the game.'
			self.socket.sendto( json.dumps(reply), address )
			
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
				receive_data, address = self.socket.recvfrom( 1024 )
				request = json.loads( receive_data )
				self.handler[request['cmd']]( self, request, address )
			except socket.error:
				pass

if __name__ == '__main__':
	ip = raw_input( "Please enter the server IP address (this is shared with clients to connect): " )
	port = raw_input( "Please enter the port to start server (leave blank for default): " )
	if len( ip ) == 0 or len( port ) == 0:
		with open( 'config/server.json') as config:
			server_configuration = json.load( config )
			ip, port = ip or server_configuration['ip'], int( port or server_configuration['port'] )
	srvr = Server( ip, int(port) )
	srvr.receive()
