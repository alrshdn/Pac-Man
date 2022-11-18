from src.game_image import GameImage
from src.board.Board import Board
from src.objects.entities.Entity import *
from tkinter import *
from math import ceil, floor


class PacMan(Entity):

    def __init__(self, root, images: GameImage, step=0.5, speed=1, position=[13, 23]):
        super().__init__(step, speed, position)
        self.root = root
        self.direction = 0
        self.images = GameImage()
        self.image = images.return_image('pacmanL')
        self.score = 0
        self.lives = 3

        self.canvas = None

        self.after_id = None

    def look(self, side: int):
        if self.direction != side:
            self.direction = side
            self.after_id = self.root.after(100, self.change_direction)

    def change_direction(self):
        self.root.after_cancel(self.after_id)
        images = self.images

        if self.direction == -1:
            self.image = images.return_image('pacmanU')
            self.position[1] -= self.step

            print("^^^")

        elif self.direction == 1:
            self.image = images.return_image('pacmanD')
            self.position[1] += self.step

            print("vvv")

        elif self.direction == 2:
            self.image = images.return_image('pacmanR')
            self.position[0] += self.step

            print(">>>")

        elif self.direction == 0 or self.direction == -2:
            self.image = images.return_image('pacmanL')
            self.move(0, -1)

            print("<<<")

        self.after_id = self.root.after(int(100/self.speed), self.change_direction)

    def move(self, axis, sign):
        if self.is_valid_move(axis, sign):
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
            print("Invalid")

    def is_valid_move(self, axis, sign):
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
                return Board.start_state[rounding_curr_pos(self.position[1])][new_pos] == 0  # at the x-axis (encoded 0)
            elif axis == 1: # Yup
                return Board.start_state[new_pos][rounding_curr_pos(self.position[0])] == 0  # at the y-axis (encoded 1)

        except IndexError:
            raise IndexError("Error")

        # when exception raised, that means block the move, and return False






# if sign > 0:
#     if start_state[][ceil(move)] == 0:
#         return True
#     return False
# elif sign < 0:
#     if start_state[floor(move)] == 0:
#         return True
#     return False

    def __unit_to_pixel(self):
        return self.position[0] * 32, self.position[1] * 32 + 2
