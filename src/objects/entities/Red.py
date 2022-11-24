from Entity import *
from src.game_image import GameImage


class Red(Entity):
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
            -1: ('blinky', 1, -1, "^^^"),
            +1: ('blinky', 1, 1, "vvv"),
            +2: ('blinky', 0, 1, ">>>"),
            -2: ('blinky', 0, -1, "<<<")
        }

        # Appearance
        self.curr_direction = None
        self.prev_direction = None
        self.image = images.return_image('blinky')

