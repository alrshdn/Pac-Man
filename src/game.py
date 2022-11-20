from window import Window
from board.Board import *
from tkinter import *
from objects.entities.Entity import *
from objects.entities.PacMan import *
from objects.entities.Ghost import *
from PIL import ImageTk, Image
import time


class Game:

    def __init__(self):
        # Static
        global window
        window = Window()
        self.board = Board()
        self.images = GameImage()

        # Movable
        self.pacman = PacMan(root=window.root, images=self.images)

    def start(self):
        self.create_board()
        self.__events_callbacks()
        self.create_entities()

        # self.create_items()
        # self.create_stats()
        return window.root

    def create_board(self):
        root = window.root

        for row in range(self.board.height):
            for column in range(self.board.width):
                is_wall = self.board.board[row][column] == 1

                canvas = Canvas(root, width=34, height=34, borderwidth=0, bd=0,
                                highlightthickness=2, highlightcolor='black', highlightbackground='black')
                canvas.configure(bg=self.board.wall_color[1])
                if is_wall:
                    canvas.create_rectangle(0, 0, 22, 22, fill=self.board.wall_color[0],outline='black')
                else:
                    canvas.create_rectangle(0, 0, 32, 32, fill=self.board.empty_color, outline='black' )

                canvas.place(width=32, height=32, x=column * 32, y=row * 32)

    def create_entities(self):
        root = window.root

        # Pac-Man
        self.pacman.canvas = Canvas(window.root, width=28, height=28, borderwidth=0, bd=0,
                                    bg=self.board.empty_color, highlightthickness=0)
        self.pacman.canvas.create_image(14, 14, image=self.pacman.image)

        self.pacman.canvas.place(x=self.pacman.position[0] * 32 + 16, y=self.pacman.position[1] * 32 + 2)
        self.pacman.canvas.delete()

    def __events_callbacks(self):
        window.root.bind('<Left>',  lambda _: self.pacman.look(-2))
        window.root.bind('<Right>', lambda _: self.pacman.look(2))
        window.root.bind('<Up>',    lambda _: self.pacman.look(-1))
        window.root.bind('<Down>',  lambda _: self.pacman.look(1))

        window.root.bind('r',       lambda _: self.pacman.restart())
