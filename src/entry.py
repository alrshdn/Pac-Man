from game import *


def entry():
    game = Game()
    game.create_board(game.window._images)
    game.window.root.mainloop()
