from objects.entities.Entity import *


class PacMan(Entity):
    def __init__(self,
                 root,
                 images: GameImage,
                 step: float,
                 speed: int,
                 position: list):
        super().__init__(root, images, step, speed, position)

        # States:
        self.__image_id = 'pacman'
        self.directions = {
            # dir_id: (axis, sign, image_name, debug_info)
            -1: (1, -1, self.__image_id + 'U', '^^^'),
            +1: (1, 1, self.__image_id + 'D', 'vvv'),
            -2: (0, -1, self.__image_id + 'L', '<<<'),
            +2: (0, 1, self.__image_id + 'R', '>>>')
        }  # override

        # Dynamics:
        self.curr_direction = -2  # override
        self.__prev_direction = None
        self.snapshot_direction = -2

        # Appearances:
        self.image = images.return_image('pacmanL')  # override

        # Stats:
        self.__score = 0
        self.__lives = 3

    def restart_callback(self):
        # Update Pac-Man's attributes to default
        self.__reset_default_attributes()

        # Re-draw
        self.__refresh_pacman()

    def move_callback(self, new_direction: int):
        if self.curr_direction != new_direction:
            print('Not Same direction')
            # logging.log(3, 'Not Same direction')  # TODO: Use a logging library
            self.__prev_direction = self.curr_direction
            self.curr_direction = new_direction
            self.__update_direction()
        else:
            print('Same directions')

    def movement(self):
        self.__update_direction()

        is_moving = self.curr_direction is not None
        if is_moving:
            axis, sign, image_name = self.directions[self.curr_direction][0:3]

            if axis == 0:
                self.x_offset(self.step * sign)
            else:
                self.y_offset(self.step * sign)

            self.__refresh_pacman(image_name)

    def __update_direction(self):
        if self.curr_direction is not None:
            self.__move(self.directions[self.curr_direction])

    def __move(self, direction: tuple):
        axis, sign, image_name, debug_info = direction

        if self.__is_valid_move(axis, sign):
            self.__prev_direction = None
            self.snap_direction = self.curr_direction
            print('Valid move')

        else:
            print('Invalid move')
            if self.__prev_direction is not None:
                self.curr_direction = self.__prev_direction
                prev_axis, prev_sign = self.directions[self.__prev_direction][0:2]

                if not self.__is_valid_move(prev_axis, prev_sign):
                    self.curr_direction = None
                else:
                    print('Valid prev_direction move')
                    self.snap_direction = self.curr_direction

                self.__prev_direction = None

            else:
                self.curr_direction = None

            print(debug_info)

    def __is_valid_move(self, axis: int, sign: int):

        # In cases of Pac-Man's half-moves:
        if self.__prev_direction is not None:
            same_axis = abs(self.curr_direction) == abs(self.__prev_direction)
            if not same_axis:
                other_axis = (axis + 1) % 2

                if self.position[other_axis] != int(self.position[other_axis]):
                    return False

        return super().is_valid_move(axis, sign)

    def __reset_default_attributes(self) -> None:
        self.image = self.images.return_image('pacmanL')
        self.position[0], self.position[1] = 13.5, 23.0
        self.curr_direction = None

    def __refresh_pacman(self, image_name='pacmanL'):
        self.image = self.images.return_image(image_name)
        super().refresh()
