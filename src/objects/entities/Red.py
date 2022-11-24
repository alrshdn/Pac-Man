from tkinter import Canvas

from src.game_image import GameImage
from src.objects.entities.Ghost import Ghost


class Red(Ghost):
    def __init__(self,
                 root,
                 images: GameImage,
                 step: float,
                 speed: int,
                 position: list,
                 target_position: list,
                 heuristic):
        super().__init__(root, step, speed, position, target_position, heuristic)

        # Core
        self.root = root

        # Appearance
        self.image = images.return_image('blinky')

    def search(self):
        pass

    def __move(self, param):
        pass

