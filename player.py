import common

from board import Board
from ship import Ship


class Player:
    def init_ships(self):
        self.ships = []
        for ship in common.SHIP_INFO:
            self.ships.append(Ship(name=ship[0], size=ship[1]))
        
    def init_boards(self):
        self.self_board = Board()
        self.enemy_board = Board()
            
    
    def __init__(self, **kwargs):
        self.name = input("Name: ")

        for key, value in kwargs.items():
            setattr(self, key, value)
        self.init_boards()
        self.init_ships()
        
