from src.board.Board import Board
from src.game_image import *  # GameImage and PhotoImage

from tkinter import Canvas
from math import ceil, floor


class Entity(object):

    def __init__(self,
                 root,
                 images: GameImage,
                 step: float,
                 speed: int,
                 position: list):
        # Core:
        self.root = root
        self.canvas = Canvas()

        # States:
        self.directions = dict()  # virtual

        # Dynamics:
        self.step = step
        self.speed = speed
        self.position = position
        self.curr_direction = None  # virtual

        # Appearances:
        self.images = images
        self.image = None  # virtual

    def x_offset(self, offset: float):
        self.position[0] += offset

    def y_offset(self, offset: float):
        self.position[1] += offset

    def unit_to_pixel(self):
        return self.position[0] * 32 + 2, self.position[1] * 32 + 2

    def is_valid_move(self, axis: int, sign: int):
        pos_on_axis = self.position[axis]
        new_pos = pos_on_axis + (self.step * sign)

        # In cases of decimal steps:
        if sign < 0:  # up and left
            rounding_new_pos = floor  # because value is decreased by a decimal step (self.step)
        else:  # down and right
            rounding_new_pos = ceil  # because value is increased by a decimal step (self.step)
        new_pos = rounding_new_pos(new_pos)

        # Trying to access board position on the new_pos position to see if it is a legal move or not:
        if axis == 1:  # changes are at the y-axis (encoded 1)
            x, y = self.position[0], new_pos
        else:  # changes are at the x-axis (encoded 0)
            x, y = new_pos, self.position[1]
        x, y = int(x), int(y)

        # In cases of out of bound on the left or the right (portals):
        if x < 0 or x > Board.width - 1:

            if self.curr_direction == 2:  # Going through the right portal
                self.position[0] = 0

            elif self.curr_direction == -2:  # Going through the left portal
                self.position[0] = Board.width - 1

            else:
                raise IndexError("Out of bounds in wrong direction!")

            return True

        return Board.start_state[y][x] == 0  # is position empty/not wall?

    def refresh(self):
        self.canvas.destroy()

        self.canvas = Canvas(self.root, width=28, height=28, borderwidth=0, bd=0,
                             bg='#161020', highlightthickness=0)

        self.canvas.create_image(14, 14, image=self.image)

        x, y = self.unit_to_pixel()
        self.canvas.place(x=x, y=y)
