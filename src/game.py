from src.window import Window
from src.board.Board import Board
from src.game_image import GameImage

from objects.entities.PacMan import PacMan
from src.objects.entities.Red import Red
from src.objects.entities.Pink import Pink

from tkinter import *
import time

global exists


class Game:
    def __init__(self):
        # Static
        self.window = Window()
        self.board = Board()
        self.images = GameImage()

        # Movable
        self.pacman = PacMan(root=self.window.root,
                             images=self.images,
                             step=0.5,
                             speed=1,
                             position=[1.0, 1.0])

        def ghost_heuristic(succession, target):
            return abs(succession[0] - target[0]) + abs(succession[1] - target[1])

        def red_target():
            return self.pacman.position

        self.red = Red(root=self.window.root,
                       images=self.images,
                       step=0.5,
                       speed=1,
                       position=[13.0, 23.0],
                       target_position=red_target(),
                       heuristic=ghost_heuristic)

        self.pink = Pink(root=self.window.root,
                         images=self.images,
                         step=0.5,
                         speed=1,
                         position=[11.0, 23.0],
                         target_position=self.pacman.position,
                         heuristic=ghost_heuristic)

    def start(self):
        self.create_board()
        self.__set_events_callbacks()
        self.create_entities()
        self.main_loop()

    def main_loop(self):
        pacman = self.pacman

        red = self.red
        pink = self.pink

        root = self.window.root
        global exists
        exists = True

        def on_closing():
            # if messagebox.askokcancel("Quit", "Do you want to quit?"):
            global exists
            exists = False

            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        while exists:  # Window is running
            pacman.movement()
            red.movement()
            pink.movement()

            time.sleep(0.1 / pacman.speed)
            root.update()

    def create_board(self):
        root = self.window.root

        for row in range(int(self.board.height)):
            for column in range(int(self.board.width)):
                is_wall = self.board.board[row][column] == 1

                canvas = Canvas(root, width=34, height=34, borderwidth=0, bd=0,
                                highlightthickness=2, highlightcolor='black', highlightbackground='black')
                canvas.configure(bg=self.board.wall_color[1])
                if is_wall:
                    canvas.create_rectangle(0, 0, 22, 22, fill=self.board.wall_color[0], outline='black')
                else:
                    canvas.create_rectangle(0, 0, 32, 32, fill=self.board.empty_color, outline='black')

                canvas.place(width=32, height=32, x=column * 32, y=row * 32)

    def create_entities(self):
        # --- Pac-Man ------------------------------------
        self.pacman.refresh()

        # --- Ghosts -------------------------------------
        # Red:
        self.red.refresh()

        # Pink:
        self.pink.refresh()
        # -------------------------------------

    def __set_events_callbacks(self):
        root = self.window.root

        # Movements
        root.bind('<Left>', lambda _: self.pacman.move_callback(-2))
        root.bind('<Right>', lambda _: self.pacman.move_callback(2))
        root.bind('<Up>', lambda _: self.pacman.move_callback(-1))
        root.bind('<Down>', lambda _: self.pacman.move_callback(1))

        # Game status
        root.bind('r', lambda _: self.pacman.restart_callback())
