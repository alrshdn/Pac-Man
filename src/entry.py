import time

from game import *


def entry():
    game = Game()
    root = game.start()
    pacman = game.pacman
    while True:

        curr_direction = pacman.curr_direction
        if isinstance(curr_direction, int):  # Not [None]
            axis, sign = pacman.directions[pacman.curr_direction][1:3]
            pacman.position[axis] += pacman.step * sign
            pacman.refresh_pacman()
            root.update()
            time.sleep(pacman.speed * 0.1)
            pacman.change_direction()
        else:
            root.update()
            # time.sleep(0.005)
