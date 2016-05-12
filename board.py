import common
import re

class Board:

    def validate_ship_fit(self, ship):
        if ship.orientation != 'v':
            max_idx = ship.col_idx + ship.size
        else:
            max_idx = ship.row_idx + ship.size

        if max_idx > common.BOARD_SIZE:
            return False
        return True

    def validate_ship_overlap(self, ship):        
        if ship.orientation != 'v':
            max_idx = ship.col_idx + ship.size
            if self.board[ship.row_idx][ship.col_idx:max_idx] != (
                common.EMPTY * ship.size):
                return False
        else:
            max_idx = ship.row_idx + ship.size
            index = ship.row_idx
            while index < max_idx:
                if self.board[index][ship.col_idx] != common.EMPTY:
                    return False                    
                index += 1
        return True
            
    def place_ship_on_board(self, player, ship):
        if ship.orientation != 'v':
            max_idx = ship.col_idx + ship.size
            self.board[ship.row_idx] = (
                self.board[ship.row_idx][:ship.col_idx] +
                common.HORIZONTAL_SHIP * ship.size
                + self.board[ship.row_idx][max_idx:])
        else:
            max_idx = ship.row_idx + ship.size
            index = ship.row_idx
            while index < max_idx:
                self.board[index] = (
                    self.board[index][:ship.col_idx] +
                    common.VERTICAL_SHIP +
                    self.board[index][ship.col_idx+1:])
                index += 1

    def validate_input(self, location, ship):
        poss_letters = "".join([
            chr(c) for c in range(ord('a'), ord('a') + common.BOARD_SIZE)])
        match = r'^[{}]\d{{1,2}}$'.format(poss_letters)
        if re.match(match, location):
            ship.col_idx = poss_letters.index(location[0])
            if len(location) == 2:
                ship.row_idx = int(location[1]) - 1
            else:
                ship.row_idx = int(location[1] + location[2]) - 1
            if ship.row_idx not in range(common.BOARD_SIZE):
                return False
        else:
            return False
        return True
                                            

    def init_board(self):
        self.board = []
        while True:
            self.board.append(common.EMPTY*common.BOARD_SIZE)
            if len(self.board) == common.BOARD_SIZE:
                break

    def __init__(self):
        self.init_board()

