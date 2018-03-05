from collections import namedtuple

Food = namedtuple('Food', ['position', 'score'])


def package_food(self):
    return {
        'position': tuple(self.position),
        'score': self.score
    }


Food.packet = package_food
