BOARD_SIZE = 4
EMPTY = 'O'


class Board:
    def get_value_at_place(self, col_idx, row_idx):
        return self.board[row_idx][col_idx]

    def put_value_at_place(self, col_idx, row_idx, value):
        self.board[row_idx] = (self.board[row_idx][:col_idx] +
                               value + self.board[row_idx][col_idx + 1:])

    def init_board(self):
        self.board = []
        while True:
            self.board.append(EMPTY * BOARD_SIZE)
            if len(self.board) == BOARD_SIZE:
                break

    def __init__(self):
        self.init_board()
