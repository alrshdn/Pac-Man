from src.objects.entities.Entity import *


class Ghost(Entity):
    def __init__(self,
                 root,
                 step: float,
                 speed: int,
                 position: list,
                 target_position: list,
                 heuristic):
        super().__init__(step, speed, position)

        self.root = root

        self.image = None
        self.directions = {
            # dir_id: (image_name, axis, sign, debug_info)
            -1: (1, -1, "^^^"),
            +1: (1, 1, "vvv"),
            +2: (0, 1, ">>>"),
            -2: (0, -1, "<<<")
        }
        self.target_position = target_position
        self.curr_direction = None
        self.heuristic = heuristic

    def agent(self):
        direction = self.search()
        self.successor(direction)

    def search(self) -> tuple:  # A*
        pass

    def successor(self, direction: tuple):
        """ Takes direction as input and makes moves by calling movement.  """
        self.movement(direction)

    def movement(self, direction: tuple):
        axis, sign = direction[0:2]
        self.position[axis] += self.step * sign
        self.refresh()

    def refresh(self):
        self.canvas.destroy()

        self.canvas = Canvas(self.root, width=28, height=28, borderwidth=0, bd=0,
                             bg='#161020', highlightthickness=0)

        self.canvas.create_image(14, 14, image=self.image)

        x, y = self.unit_to_pixel()
        self.canvas.place(x=x, y=y)
