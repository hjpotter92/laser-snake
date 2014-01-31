class Player:
	def __init__( self, username = "" ):
		self.nick = username

	def getPlayerId( self ):
		return self.player_id

	def setPlayerId( self, playerid ):
		self.player_id = playerid

	def getNick( self ):
		return self.nick
