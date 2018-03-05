from time import time

from rencode import loads

__all__ = ['TIME', 'parse_packet']

TIME = lambda: int(time())


def parse_packet(data):
    def decode(obj):
        if isinstance(obj, bytes):
            return obj.decode()
        if isinstance(obj, dict):
            return {
                k.decode(): decode(v)
                for k, v in obj.items()
            }
        return obj
    data = loads(data)
    return decode(data)
