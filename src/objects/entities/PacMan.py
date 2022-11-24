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
            self.change_direction()
            # Starting event cycle
        else:
            print('Same directions')

    def change_direction(self):
        if isinstance(self.curr_direction, int):
            self.__move(self.directions[self.curr_direction])

    def __move(self, direction: tuple):
        image_name, axis, sign, debug_info = direction

        is_valid_move = self.__is_valid_move(axis, sign)
        if is_valid_move:
            self.prev_direction = None
            print('Valid move')

        elif isinstance(is_valid_move, bool):  # False : - same axis | not same axis

            print('Not valid move')
            if isinstance(self.prev_direction, int):
                self.curr_direction = self.prev_direction
                prev_axis, prev_sign = self.directions[self.prev_direction][1:3]
                if self.__is_valid_move(prev_axis, prev_sign):
                    self.prev_direction = None
                    print('Valid prev_direction move')
                else:
                    self.prev_direction = None
                    self.curr_direction = None
            else:
                self.prev_direction = None
                self.curr_direction = None

        print(debug_info)

    def __is_valid_move(self, axis: int, sign: int):
        # valid move?
        # True: change the direction
        # False: prev_direction != None?
        # is valid move for prev_direction?
        # True: change the direction
        # False: direction = None
        # False: direction = None

        # if isinstance(self.prev_direction, int):
        #     is_same_axis = abs(self.curr_direction) == abs(self.prev_direction)
        #     print('is_same_axis', is_same_axis)
        #     if not is_same_axis:
        #         self.position[axis] += sign
        #         if Board.start_state[int(self.position[0])][int(self.position[1])] == 1:
        #             self.position[axis] -= sign
        #             self.curr_direction = self.prev_direction
        #             return None
        #         self.position[axis] -= sign

        # if not is_same_axis:  # Returns True if float position at axis is an integer
        #     if isinstance(self.position[int(axis == 0)], int) or not self.position[int(axis == 0)].is_integer():
        #         self.curr_direction = self.prev_direction
        #         self.position[(axis + 1) % 2] += self.step * self.directions[self.curr_direction][2]
        #     # Re-draw
        #     return None

        if isinstance(self.prev_direction, int):  # checking [Half moves] case
            same_axis = abs(self.curr_direction) == abs(self.prev_direction)
            if not same_axis:
                other_axis = (axis + 1) % 2
                other_axis = self.position[other_axis]
                if other_axis != int(other_axis):
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

            return None
        # when exception raised, that means moving from gate

    def restart(self):  # Needs to implement event loop restart
        print('restart game')

        # Update attributes to default
        self.__reset_default_attributes()

        # Re-draw
        self.refresh_pacman()

    def __reset_default_attributes(self) -> None:
        self.image = self.images.return_image('pacmanL')
        self.position = [13.5, 23]
        self.curr_direction = None

    def refresh_pacman(self):
        self.canvas.destroy()
        self.canvas = Canvas(self.root, width=28, height=28, borderwidth=0, bd=0,
                             bg='#161020', highlightthickness=0)
        self.image = self.images.return_image(self.directions[self.curr_direction][0])
        self.canvas.create_image(14, 14, image=self.image)

        x, y = self.__unit_to_pixel()
        self.canvas.place(x=x, y=y)

    def __unit_to_pixel(self):
        return self.position[0] * 32 + 2, self.position[1] * 32 + 2
