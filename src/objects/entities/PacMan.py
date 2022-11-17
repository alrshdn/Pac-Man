from src.game_image import GameImage
from src.objects.entities.Entity import *
from tkinter import *


class PacMan(Entity):

    def __init__(self, root, images: GameImage, step=0.5, speed=1, position=[13, 23]):
        super().__init__(step, speed, position)
        self.root = root
        self.direction = 0
        self.images = GameImage()
        self.image = images.return_image('pacmanL')
        self.score = 0
        self.lives = 3

        self.canvas = None

        self.after_id = None

    def look(self, side: int):
        if self.direction != side:
            self.direction = side
            self.after_id = self.root.after(1000, self.change_direction)

    def change_direction(self):
        self.root.after_cancel(self.after_id)
        images = self.images
        self.canvas.destroy()
        self.canvas = Canvas(self.root, width=28, height=28, borderwidth=0, bd=0,
                             bg='#161020', highlightthickness=0)

        if self.direction == 1:
            self.image = images.return_image('pacmanU')
            self.position[1] -= self.step

            print("^^^")

        elif self.direction == -1:
            self.image = images.return_image('pacmanD')
            self.position[1] += self.step

            print("vvv")

        elif self.direction == 2:
            self.image = images.return_image('pacmanR')
            self.position[0] += self.step

            print(">>>")

        elif self.direction == 0 or self.direction == -2:
            self.image = images.return_image('pacmanL')
            self.position[0] -= self.step

            print("<<<")

        # Update image
        self.canvas.create_image(14, 14, image=self.image)

        # Update position
        x, y = self.__unit_to_pixel()
        self.canvas.place(x=x, y=y)

        self.after_id = self.root.after(int(100/self.speed), self.change_direction)

    def __unit_to_pixel(self):
        return self.position[0] * 32, self.position[1] * 32 + 2
