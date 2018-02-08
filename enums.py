from enum import Enum
from random import choice

from vector import Vector


class Colours(Enum):
    BACKGROUND = (45, 45, 45)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    @classmethod
    def RANDOM(cls):
        return choice([
            color for color in cls
            if color not in (
                cls.BACKGROUND, cls.WHITE, cls.BLACK
            )
        ])


class Direction(Enum):
    """docstring for Direction"""
    RIGHT = Vector((1, 0))
    UP = Vector((0, -1))
    LEFT = Vector((-1, 0))
    DOWN = Vector((0, 1))
    BOTTOM_RIGHT = RIGHT + DOWN

    @classmethod
    def RANDOM(cls):
        return choice([
            cls.UP, cls.LEFT,
            cls.DOWN, cls.RIGHT
        ])
