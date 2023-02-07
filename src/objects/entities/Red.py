from objects.entities.Ghost import Ghost
from game_image import GameImage


class Red(Ghost):
    def __init__(self,
                 root,
                 images: GameImage,
                 step: float,
                 speed: int,
                 position: list,
                 target_position,
                 heuristic):
        super().__init__(root, images, step, speed, position, target_position, heuristic)

        # Appearance
        self.image = images.return_image('blinky')
