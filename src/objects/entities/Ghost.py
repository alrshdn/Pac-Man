from src.objects.entities.Entity import *


class Ghost(Entity):

    def __init__(self, speed: int, position: tuple, g_id: int):
        super().__init__(speed, position)
        self.id = g_id
        self.state = 0

        if self.id == 1:
            self.direction = None
            self.image = None
        elif self.id == 2:
            self.direction = None
            self.image = None
        elif self.id == 3:
            self.direction = None
            self.image = None
        elif self.id == 4:
            self.direction = None
            self.image = None

    def movement(self):
        pass
