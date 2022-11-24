from objects.entities.PacMan import *
from src.objects.entities.Red import Red
from window import Window

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

        self.red = Red(root=self.window.root,
                       images=self.images,
                       step=0.5,
                       speed=1,
                       position=[13.0, 23.0],
                       target_position=[1.0, 1.0],
                       heuristic= None)

    def start(self):
        self.create_board()
        self.__set_events_callbacks()
        self.create_entities()
        self.main_loop()

    def main_loop(self):
        pacman = self.pacman

        red = self.red

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
            # red.movement()

            time.sleep(pacman.speed * 0.1)
            root.update()

    def create_board(self):
        root = self.window.root

        for row in range(self.board.height):
            for column in range(self.board.width):
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
        # Pac-Man
        self.pacman.refresh_pacman()

        # -------------------------------------
        # Red
        self.red.canvas = Canvas(self.window.root, width=28, height=28, borderwidth=0, bd=0,
                                    bg=self.board.empty_color, highlightthickness=0)
        self.red.canvas.create_image(14, 14, image=self.red.image)

        self.red.canvas.place(x=self.red.position[0] * 32 + 2, y=self.red.position[1] * 32 + 2)
        self.red.canvas.delete()

    def __set_events_callbacks(self):
        root = self.window.root

        # Movements
        root.bind('<Left>', lambda _: self.pacman.move_callback(-2))
        root.bind('<Right>', lambda _: self.pacman.move_callback(2))
        root.bind('<Up>', lambda _: self.pacman.move_callback(-1))
        root.bind('<Down>', lambda _: self.pacman.move_callback(1))

        # Game status
        root.bind('r', lambda _: self.pacman.restart())
