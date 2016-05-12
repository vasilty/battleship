import common

from player import Player

        
class Game():

    def put_ship(self, player, ship, message=None):
        poss_letters = "".join([
            chr(c) for c in range(ord('a'), ord('a') + common.BOARD_SIZE)])
        message_input = ('Invalid location! Letters a - {} and '
                         'numbers 1 - {} are allowed (eg. a1)').format(
                             poss_letters[-1], common.BOARD_SIZE)
        message_fit = ('Invalid ship location! The ship does not fit ' \
                     'on the board')
        message_overlap = ('Invalid ship location! The ship overlaps ' \
                     'with another ship.')
        
        common.clear_screen()
        common.print_board(player.self_board.board)
        if message:
            print(message)
        location = input('{}, place the location of the {} ({} spaces): '
                         .format(player.name,
                                 ship.name,
                                 ship.size)).lower().strip()
        if not player.self_board.validate_input(location=location, ship=ship):
            return self.put_ship(player=player,
                                 ship=ship,
                                 message=message_input)
        ship.orientation = input('Is it horizontal or vertical? (H)/V '
                            ).lower().strip()
        if not player.self_board.validate_ship_fit(ship=ship):
            return self.put_ship(player=player,
                                 ship=ship,
                                 message=message_fit)
        if not player.self_board.validate_ship_overlap(ship=ship):      
            return self.put_ship(player=player,
                                 ship=ship,
                                 message=message_overlap)
        player.self_board.place_ship_on_board(player=player, ship=ship)
        ship.make_occup_list()

    def put_ships(self, player):
        input('{}, it is time to place your ships! '\
              'Press enter to continue. '.format(player.name))
        for ship in player.ships:
            self.put_ship(player=player, ship=ship)
            common.clear_screen()
            common.print_board(player.self_board.board)
            print(ship.occup)
        input('{}, you have placed all your ships. ' \
              'Press enter to continue. '.format(player.name))
        common.clear_screen()

    def __init__(self):
        common.clear_screen()
        print('Player 1 ', end='')
        player1 = Player()
        print('Player 2 ', end='')
        player2 = Player()
        players = [player1, player2]
        common.clear_screen()
        for player in players:
            self.put_ships(player=player)
        input('The Battle begins! Press enter to continue.')
        common.clear_screen()
        while True:
            for player in players:
                input("It is {}'s turn! Press enter to continue. ".format(
                    player.name))
                common.clear_screen()
            break
        


Game()
    
