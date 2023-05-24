import random
from tkinter import Canvas
from board.Board import Board
from objects.entities.Ghost import *


class Orange(Ghost):
    def __init__(self,
                 root,
                 images: GameImage,
                 step: float,
                 speed: int,
                 position: list,
                 pacman_position,
                 heuristic):

        def in_circle():
            """
            The distance between the two points is calculated using the Manhattan distance metric,
            which is the sum of the absolute differences in the x and y coordinates of the two points.
            If this distance is less than or equal to 8,
            the function returns True, indicating that the point is within the specified radius of the target.
            Otherwise, the function returns False, indicating that the point is outside the radius.
            """
            manhattan_distance = abs(self.position[0] - pacman_position[0]) + \
                abs(self.position[1] - pacman_position[1])

            return manhattan_distance <= 8

        def orange_target_getter():

            if in_circle():
                x = random.randint(0, Board.width)
                y = random.randint(0, Board.height)
                return [x, y]
            else:
                return pacman_position
        self.c = Canvas(root, width=80, height=80)

        super().__init__(root, images, step, speed,
                         position, orange_target_getter, heuristic)

        # Appearance
        self.image = images.image_getter('clyde')
