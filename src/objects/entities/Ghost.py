from game_image import GameImage
from objects.entities.Entity import Entity


class Ghost(Entity):
    def __init__(self,
                 root,
                 images: GameImage,
                 step: float,
                 speed: int,
                 position: list,
                 target_getter,
                 heuristic):
        super().__init__(root, images, step, speed, position)

        # States:
        self.directions = {
            # dir_id: (axis, sign, debug_info)
            -1: (1, -1, "^^^"),
            +1: (1, 1, "vvv"),
            -2: (0, -1, "<<<"),
            +2: (0, 1, ">>>")
        }  # override

        # Dynamics:
        self.curr_direction = -1  # override

        # Artificial Intelligence:
        self.heuristic = heuristic
        self.target_getter = target_getter

        self.target_position = None
        #  self.point_canvas = Canvas()

    def movement(self):
        new_direction = self.search()
        self.curr_direction = new_direction

        self.successor(self.directions[new_direction])

    def search(self):
        """
        -   Action Space:
            UP/DOWN/LEFT/RIGHT (encoded as -1, +1, -2, and +2 respectively).
        -   State Space:
            All possible (x, y) positions the ghost can be at.
        -   Goal:
            Reaching target position.
        -   Strategy:
            Greedy Search (Best First Search)
        -   Heuristic:
            Dynamic (will change based on the inputted heuristic argument in the initializer).
        :return: int (encoded direction)
        """

        # List all the possible states of the next move (successions):
        successions = list()
        directions = list()

        for key in list(self.directions.keys())[0:2]:  # Up and Down
            axis, sign = self.directions[key][0:2]

            is_opposite = self.curr_direction == -1 * key
            if self.__is_valid_move(axis, sign) and not is_opposite:
                successions.append([self.position[0], self.position[1] + key])
                directions.append(key)

        for key in list(self.directions.keys())[2:]:  # Left and Right
            axis, sign = self.directions[key][0:2]

            is_opposite = self.curr_direction == -1 * key
            if self.__is_valid_move(axis, sign) and not is_opposite:
                successions.append([self.position[0] + key, self.position[1]])
                directions.append(key)

        # Get current target position:
        self.target_position = self.target_getter()

        # Calculate the cost of all the successions using the heuristic function:
        costs = list()
        for succession in successions:
            cost = self.heuristic(succession, self.target_position)
            costs.append(cost)

        # Choose the succession with the least cost:
        succession_index = costs.index(min(costs))
        succession_direction = directions[succession_index]

        # Return the direction of movement:
        return succession_direction

    def successor(self, direction_info: tuple):
        """ Takes direction as input and makes moves by calling movement.  """
        axis, sign = direction_info[0:2]

        if axis == 0:
            self.x_offset(self.step * sign)
        else:
            self.y_offset(self.step * sign)

        self.__refresh_ghost()

    def __is_valid_move(self, axis: int, sign: int):

        # In cases of ghost's half-moves:
        other_axis = (axis + 1) % 2
        if self.position[other_axis] != int(self.position[other_axis]):
            return False

        return super().is_valid_move(axis, sign)

    def __refresh_ghost(self):
        super().refresh()
