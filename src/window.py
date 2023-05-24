from tkinter import *


class Window:

    def __init__(self):
        self.root = Tk()
        self.root.configure(bg='black')
        self.window_width = 896
        self.window_height = 992

        self.root.minsize(self.window_width, self.window_height)
        self.root.maxsize(self.window_width, self.window_height)
