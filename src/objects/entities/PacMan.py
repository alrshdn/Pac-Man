from tkinter import *
from math import ceil, floor

from src.board.Board import Board
from src.game_image import GameImage
from src.objects.entities.Entity import Entity


class PacMan(Entity):
    def __init__(self,
                 root,
                 images: GameImage,
                 step: float,
                 speed: int,
                 position: list):
        super().__init__(step, speed, position)

        # Core
        self.root = root
        self.images = images
        self.canvas = None
        self.after_id = None

        # States
        self.directions = {
            # dir_id: (image_name, axis, sign, debug_info)
            -1: ('pacmanU', 1, -1, "^^^"),
            +1: ('pacmanD', 1, 1, "vvv"),
            +2: ('pacmanR', 0, 1, ">>>"),
            -2: ('pacmanL', 0, -1, "<<<")
        }

        # Appearance
        self.curr_direction = None
        self.prev_direction = None
        self.image = images.return_image('pacmanL')

        # Stats
        self.score = 0
        self.lives = 3

    def move_callback(self, new_direction: int):
        if self.curr_direction != new_direction:
            print('Not Same directions')
            self.prev_direction = self.curr_direction
            self.curr_direction = new_direction

            # Starting event cycle
            self.after_id = self.root.after(100, self.__change_direction)

        else:
            print('Same directions')

    def __change_direction(self):
        self.root.after_cancel(self.after_id)

        self.__move(self.directions[self.curr_direction])

        self.after_id = self.root.after(int(100 / self.speed), self.__change_direction)

    def __move(self, direction: tuple):
        image_name, axis, sign, debug_info = direction

        self.image = self.images.return_image(image_name)

        if self.__is_valid_move(axis, sign):
            # Move
            self.position[axis] += self.step * sign
            # Re-draw
            self.__refresh_pacman()

        else:  # False : - same axis | not same axis
            print('else')
            # if self.prev_direction != self.curr_direction:
            #     if (self.prev_direction in (-2, 2) and axis != 0) or \
            #             (self.prev_direction in (-1, 1) and axis != 1):
            #         print('else- if ')
                    # self.position[(axis + 1) % 2] += self.step * sign
                    # self.__refresh_pacman()

            # Cancel past event cycle
            # TODO fix event cycle not stopping after:

        print(debug_info)

    def __is_valid_move(self, axis: int, sign: int):
        if not self.position[int(axis == 0)].is_integer():  # Returns True if float position at axis is an integer
            return False

        pos_on_axis = self.position[axis]

        new_pos = pos_on_axis + (self.step * sign)

        # in cases of decimal steps:
        if sign < 0:  # up and left
            rounding_new_pos = floor  # because value is decreased by a decimal step (self.step)
        else:  # down and right=
            rounding_new_pos = ceil  # because value is increased by a decimal step (self.step)

        new_pos = rounding_new_pos(new_pos)

        # Trying to access board position on the new_pos position to see if it is a legal move or not:
        try:

            if axis == 1:  # changes are at the y-axis (encoded 1)
                x, y = self.position[0], new_pos
            else:  # changes are at the x-axis (encoded 0)
                x, y = new_pos, self.position[1]

            x, y = int(x), int(y)

            if x < 0:  # Out of bounds on the left
                x = ~x + Board.width  # Enforcing IndexError

            return Board.start_state[y][x] == 0  # is position empty/not wall?

        except IndexError:  # In cases of gates
            print("IndexError")
            if self.curr_direction == 2:  # Going through the right portal
                self.position = [-1, self.position[1]]

            elif self.curr_direction == -2:  # Going through the left portal
                self.position = [Board.width, self.position[1]]

            else:
                raise IndexError("Error")

            return True
        # when exception raised, that means moving from gate

    def restart(self):  # Needs to implement event loop restart
        print('restart game')
        # Cancel past event cycle
        self.root.after_cancel(self.after_id)

        # Update attributes to default
        self.__reset_default_attributes()

        # Re-draw
        self.__refresh_pacman()

    def __reset_default_attributes(self) -> None:
        self.image = self.images.return_image('pacmanL')
        self.position = [13.5, 23]
        self.curr_direction = None

    def __refresh_pacman(self):
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

    def __unit_to_pixel(self):
        return self.position[0] * 32 + 2, self.position[1] * 32 + 2
