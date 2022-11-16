from src.game_image import GameImage
from src.objects.entities.Entity import *


class PacMan(Entity):
    images = []

    def __init__(self, speed=0.5, position=(0, 3)):
        super().__init__(speed, position)
        self.direction = 0
        self.images = GameImage()
        self.score = 0
        self.lives = 3
        self.direction_image()
    def look_up(self):
        self.direction = 1

    def look_down(self):
        self.direction = -1

    def look_right(self):
        self.direction = 2

    def look_left(self):
        self.direction = -2
    def direction_image(self):
        images = self.images
        if self.direction == 0 or self.direction == 2:
            self._image = images.return_image('pacmanR')

        elif self.direction == -2:
            self._image = images.return_image('pacmanL')

        elif self.direction == -1:
            self._image = images.return_image('pacmanD')

        elif self.direction == 1:
            self._image = images.return_image('pacmanU')