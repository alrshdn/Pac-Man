from tkinter import Canvas


class Entity(object):

    def __init__(self, step: float, speed: int, position: list):
        self.step = step
        self.speed = speed
        self.position = list(position)
        self.canvas = Canvas()
        self.directions = dict()

    def x_offset(self, offset: int):
        self.position[1] += offset

    def y_offset(self, offset: int):
        self.position[0] += offset
