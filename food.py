class Food:
    """docstring for Food"""
    def __init__(self, position, score=1, color=None):
        self.position = position
        self.score = score
        self.color = color

    def get_position(self):
        return self.position

    def get_score(self):
        return self.score

    def get_color(self):
        return self.color.value
