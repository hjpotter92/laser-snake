import json

def send( channel, message, address ):
	try:
		channel.sendto( json.dumps(message), address )
		return True
	except OSError as e:
		print e
		return False

def receive( channel, packet_size = 1024 ):
	try:
		data, address = channel.recvfrom( int(packet_size) )
		return ( json.loads(data), address )
	except OSError as e:
		print e
		return False
