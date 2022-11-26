from src.objects.entities.Ghost import *


class Orange(Ghost):
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
        self.image = images.return_image('clyde')

    def in_circle(self):
        if abs(self.point_canvas[0] - self.target_position[0]) + \
                abs(self.point_canvas[1] - self.target_position[1]) <= 8:
            return True

    def orange_target_getter(self):
        pass
