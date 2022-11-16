class Entity(object):

    def __init__(self, speed: int, position: tuple):
        self.speed = speed
        self.position = position

    def x_offset(self, offset: int):
        self.position[0] += offset

    def y_offset(self, offset: int):
        self.position[1] += offset
