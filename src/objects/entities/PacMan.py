from tkinter import *
from math import ceil, floor

from src.board.Board import Board
from src.game_image import GameImage
from src.objects.entities.Entity import Entity


class PacMan(Entity):

    def __init__(self,
                 root,
                 images: GameImage,
                 step=0.5,
                 speed=1,
                 position=[0.5, 1]):

        super().__init__(step, speed, position)

        # Core
        self.root = root
        self.images = images
        self.canvas = None
        self.after_id = None

        # Appearance
        self.direction = 0
        self.image = images.return_image('pacmanL')

        # Stats
        self.score = 0
        self.lives = 3

    def look(self, side: int):
        if self.direction != side:
            self.prev_direction = self.direction
            self.direction = side
            self.after_id = self.root.after(100, self.__change_direction)

    def __change_direction(self):
        self.root.after_cancel(self.after_id)

        images = self.images

        if self.direction == -1:
            self.image = images.return_image('pacmanU')
            self.__move(1, -1)

            print("^^^")

        elif self.direction == 1:
            self.image = images.return_image('pacmanD')
            self.__move(1, 1)

            print("vvv")

        elif self.direction == 2:
            self.image = images.return_image('pacmanR')
            self.__move(0, 1)

            print(">>>")

        elif self.direction == 0 or self.direction == -2:
            self.image = images.return_image('pacmanL')
            self.__move(0, -1)

            print("<<<")

        self.prev_direction = self.direction

        self.after_id = self.root.after(int(100/self.speed), self.__change_direction)

    def __move(self, axis, sign):
        if self.__is_valid_move(axis, sign):
            self.position[axis] += self.step * sign

            # Destroy
            self.canvas.destroy()

            # Recreate Canvas
            self.canvas = Canvas(self.root, width=28, height=28, borderwidth=0, bd=0,
                                 bg='#161020', highlightthickness=0)

            # Update image
            self.canvas.create_image(14, 14, image=self.image)

            # Update position and re-draw
            x, y = self.__unit_to_pixel()
            self.canvas.place(x=x, y=y)

        else:
            self.direction = self.prev_direction
            self.__change_direction()

    def __is_valid_move(self, axis, sign: int):
        pos_on_axis = self.position[axis]

        new_pos = pos_on_axis + (self.step * sign)

        # in cases of decimal steps:
        if sign > 0:
            rounding_new_pos = ceil  # because value is increased by a decimal step (self.step)
            rounding_curr_pos = floor
        elif sign < 0:
            rounding_new_pos = floor  # because value is decreased by a decimal step (self.step)
            rounding_curr_pos = ceil

        new_pos = rounding_new_pos(new_pos)

        # trying to access board position on the new_pos position to see if it is a legal move or not:
        try:
            if axis == 0:
                x, y = new_pos, rounding_curr_pos(self.position[1])  # changes are at the x-axis (encoded 0)
            elif axis == 1:
                x, y = rounding_curr_pos(self.position[0]), new_pos  # changes are at the y-axis (encoded 1)

            return Board.start_state[y][x] == 0  # is position empty/not wall?

        except IndexError:
            if self.direction == 2:
                self.position = [13, 23]

            elif self.direction == -2:
                self.position = [0, 14]

            else:
                raise IndexError("Error")

        # when exception raised, that means block the move, and return False

    def restart(self):
        self.position = [13, 23]

    def __unit_to_pixel(self):
        return self.position[0] * 32, self.position[1] * 32 + 2
