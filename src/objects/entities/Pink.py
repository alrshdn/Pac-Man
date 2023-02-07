from objects.entities.Ghost import *


class Pink(Ghost):
    def __init__(self,
                 root,
                 images: GameImage,
                 step: float,
                 speed: int,
                 position: list,
                 target_position: list,
                 heuristic):
        super().__init__(root, images, step, speed, position, target_position, heuristic)

        # Appearance
        self.image = images.return_image('pinky')
