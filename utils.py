from time import time

from rencode import loads

__all__ = ['TIME', 'parse_packet']

TIME = lambda: int(time())


def parse_packet(data):
    data = loads(data)
    return {
        k.decode(): v.decode() if isinstance(v, bytes) else v
        for k, v in data.items()
    }
