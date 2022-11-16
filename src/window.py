from tkinter import *


class Window:

    def __init__(self):
        self.root = Tk()
        self.root.configure(bg='black')
        self.window_width = 896 + 4*28
        self.window_height = 992 + 4*31

        self.root.minsize(self.window_width, self.window_height)
        self.root.maxsize(self.window_width, self.window_height)
        from src.game_image import GameImage
        self._images= GameImage()