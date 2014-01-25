import uuid
from snake import Snake

class Player:
	def __init__( self, username = "" ):
		self.nick = username
		self.player_id = uuid.uuid4()

	def getplayerid( self ):
		return self.player_id

	def setplayerid( self, playerid ):
		self.player_id = playerid

	def getNick( self ):
		return self.nick
