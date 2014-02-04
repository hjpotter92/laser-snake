class Player:
	def __init__( self, username, playerid = 0 ):
		self.nick = username
		if playerid != 0:
			self.player_id = playerid

	def getPlayerId( self ):
		return self.player_id

	def setPlayerId( self, playerid ):
		self.player_id = playerid

	def getNick( self ):
		return self.nick
