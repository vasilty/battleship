import common

from board import Board
from ship import Ship

SHIP_INFO = [
    #    ("Aircraft Carrier", 5),
    #    ("Battleship", 4),
    #    ("Submarine", 3),
    ("Cruiser", 3),
    ("Patrol Boat", 2)
]


class Player:
    def init_ships(self):
        self.ships = []
        for ship in SHIP_INFO:
            self.ships.append(Ship(name=ship[0], size=ship[1]))

    def init_boards(self):
        self.self_board = Board()
        self.guess_board = Board()

    def get_name(self, message=None):
        if message:
            print(message)
        name = input("Name: ").strip()
        if len(name) == 0:
            message = "Name should contain at least one character."
            self.get_name(message=message)
        else:
            self.name = name

    def __init__(self):
        self.opponent = None
        self.get_name()
        self.init_boards()
        self.init_ships()
