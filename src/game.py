from window import Window
from board.Board import *
from tkinter import *
from objects.entities.Entity import *
from objects.entities.PacMan import *
from objects.entities.Ghost import *
from PIL import ImageTk, Image


class Game:

    def __init__(self, ):
        self.window = Window()
        self.board = Board()
        self.pacman = PacMan()

    def create_board(self):
        root = self.window.root

        for row in range(self.board.height):
            for column in range(self.board.width):
                is_wall = self.board.board[row][column] == 1
                canvas = Canvas(root, width=32, height=32, borderwidth=0, bd=0, highlightthickness=0)
                canvas.configure(bg=self.board.wall_color[1])
                if is_wall:
                    canvas.create_rectangle(0, 0, 22, 22, fill=self.board.wall_color[0])
                else:
                    canvas.create_rectangle(0, 0, 32, 32, fill=self.board.empty_color)

                canvas.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)
        frame = Frame(root, width=32, height=32)
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.5)

        img = ImageTk.PhotoImage(Image.open("forest.jpg"))
        label = Label(frame, image=img)
        pac_position = self.pacman.position
        label.grid(row=pac_position[0], column=pac_position[1])

    def start(self):
        self.create_board()

    def __listen_to_events(self):
        self.window.root.bind('<Left>', self.pacman.look_left())
        self.window.root.bind('<Right>', self.pacman.look_right())
        self.window.root.bind('<Up>', self.pacman.look_up())
        self.window.root.bind('<Down>', self.pacman.look_down())
