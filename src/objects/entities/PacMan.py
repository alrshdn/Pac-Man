from logging import log
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
                 position=(0.5, 1)):  # TODO [fixed] default parameters should be immutable

        super().__init__(step, speed, position)

        # Core

        self.root = root
        self.images = images
        self.canvas = None
        self.after_id = None

        # Appearance
        # TODO change name and value change from 0 to -2
        self.current_direction = -2
        self.image = images.return_image('pacmanL')

        # Stats
        self.score = 0
        self.lives = 3
        # TODO change -> init prev_direction field
        self.prev_direction = None

    # TODO change names
    def event_callback(self, new_direction: int):
        if self.current_direction != new_direction:
            print('- Different directions')
            self.prev_direction = self.current_direction
            self.current_direction = new_direction
            self.after_id = self.root.after(100, self.__change_direction)
        else:
            print('= Same directions')

    def __change_direction(self):
        self.root.after_cancel(self.after_id)

        directions = {
            -1: ('pacmanU', 1, -1, "^^^"),
            1: ('pacmanD', 1, 1, "vvv"),
            2: ('pacmanR', 0, 1, ">>>"),
            -2: ('pacmanL', 0, -1, "<<<")
        }
        self.__move(directions[self.current_direction])

        self.after_id = self.root.after(int(100 / self.speed), self.__change_direction)

    def __move(self, tuple_of_data: tuple):
        image_name, axis, sign, debug_text = tuple_of_data
        self.image = self.images.return_image(image_name)
        image_name, axis, sign, debug_text = tuple_of_data

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
            self.current_direction = self.prev_direction
            self.__change_direction()
        print(debug_text)

    def __is_valid_move(self, axis, sign: int):
        pos_on_axis = self.position[axis]

        new_pos = pos_on_axis + (self.step * sign)

        # in cases of decimal steps:
        # TODO Change
        rounding_new_pos = floor  # because value is decreased by a decimal step (self.step)
        rounding_curr_pos = ceil
        if sign > 0:
            rounding_new_pos = ceil  # because value is increased by a decimal step (self.step)
            rounding_curr_pos = floor
        new_pos = rounding_new_pos(new_pos)

        # trying to access board position on the new_pos position to see if it is a legal move or not:
        try:
            # TODO Change
            x, y = rounding_curr_pos(self.position[0]), new_pos  # changes are at the y-axis (encoded 1)
            if axis == 0:
                x, y = new_pos, rounding_curr_pos(self.position[1])  # changes are at the x-axis (encoded 0)

            return Board.start_state[y][x] == 0  # is position empty/not wall?

        except IndexError:
            if self.current_direction == 2:
                self.position = [13, 23]

            elif self.current_direction == -2:
                self.position = [0, 14]

            else:
                raise IndexError("Error")

        # when exception raised, that means moving from gate

    def restart(self):  # Needs to implement event loop restart
        print('restart game')
        # self.position = [13, 23]
        # # TODO add some default values
        # self.image = self.images.return_image('pacmanL')
        # self.current_direction = None
        # self.prev_direction = None
        # OR just do this
        self.__init__(root=self.root, images=self.images)

    def __unit_to_pixel(self):
        return self.position[0] * 32, self.position[1] * 32 + 2
