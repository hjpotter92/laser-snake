from random import randint


class Vector(tuple):
    def __add__(self, other):
        return Vector(v + w for v, w in zip(self, other))

    def __radd__(self, other):
        return Vector(w + v for v, w in zip(self, other))

    def __sub__(self, other):
        return Vector(v - w for v, w in zip(self, other))

    def __rsub__(self, other):
        return Vector(w - v for v, w in zip(self, other))

    def __mul__(self, s):
        return Vector(v * s for v in self)

    def __rmul__(self, s):
        return Vector(v * s for v in self)

    def __neg__(self):
        return -1 * self

    def __floordiv__(self, s):
        return Vector(v // s for v in self)


def random_vector(topleft, bottomright, exceptions=None):
    ranges = list(zip(topleft, bottomright))
    exceptions = list(map(Vector, set(exceptions or [])))
    while True:
        point = Vector(tuple(randint(*x) for x in ranges))
        if point not in exceptions:
            return point
    return point
