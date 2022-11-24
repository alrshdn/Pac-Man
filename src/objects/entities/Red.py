from tkinter import Canvas

from src.game_image import GameImage
from src.objects.entities.Ghost import Ghost


class Red(Ghost):
    def __init__(self,
                 root,
                 images: GameImage,
                 step: float,
                 speed: int,
                 position: list):
        super().__init__(step, speed, position)

        # Core
        self.root = root

        # Appearance
        self.curr_direction = None
        self.prev_direction = None
        self.image = images.return_image('blinky')

    def search(self):
        pass

    def __move(self, param):
        pass

