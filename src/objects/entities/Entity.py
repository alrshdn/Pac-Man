class Entity(object):

    def __init__(self, step: int, speed: int, position: list):
        self.step = step
        self.speed = speed
        self.position = list(position)  # TODO fix default value should be immutable

    def x_offset(self, offset: int):
        self.position[0] += offset

    def y_offset(self, offset: int):
        self.position[1] += offset
