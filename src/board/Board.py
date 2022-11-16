empty = 0
wall = 1

start_state = [
    [],
    [],
    [],
    []
]


class Board(object):
    def __init__(self):
        self.board = list()

    def create_board(self):
        for l in start_state:
            self.board.append(l)


    pass

