import re
from board import BOARD_SIZE, EMPTY
from player import Player

VERTICAL_SHIP = '|'
HORIZONTAL_SHIP = '-'
MISS = '.'
HIT = '*'
SUNK = '#'

error_input = ('Invalid location {}! Letters a - {} and '
               'numbers 1 - {} are allowed (eg. a1)')
error_fit = ('Invalid location {}! The ship does not fit '
             'on the board.')
error_overlap = ('Invalid location {}! The ship overlaps '
                 'with another ship.')
error_visited = 'Location {} has already been visited! Try again.'


def clear_screen():
    print("\033c", end="")


def print_board_heading():
    print("   " + " ".join([chr(c) for c in range(ord('A'), ord('A') +
                                                  BOARD_SIZE)]))


def print_board(board):
    print_board_heading()
    row_num = 1
    for row in board:
        print(str(row_num).rjust(2) + " " + (" ".join(row)))
        row_num += 1


def clear_and_print_two_boards(board1, board2):
    clear_screen()
    print_board(board1)
    print('')
    print_board(board2)
    print('')


def clear_and_print_one_board(board):
    clear_screen()
    print_board(board)
    print('')


def get_idx_from_location(location):
    """Returns tuple (column index, row index) from the input data."""
    alph = 'abcdefghijklmnopqrstuvwxyz'
    col_idx = alph.index(location[0])
    row_idx = int(location[1:]) - 1
    return col_idx, row_idx


def put_ship(player, ship, message=None):
    """Gets the ship location and orientation from the user.
    Validates the input and checks whether the ship can be placed on the
    board. If it is possible, places the ship on the user's board,
    if it is not possible, the function is run again."""
    clear_and_print_one_board(player.self_board.board)
    if message:
        print(message)
    location = ''.join(input('{}, select a location of a {} ({} spaces): '
                             .format(player.name,
                                     ship.name,
                                     ship.size)).lower().strip().split())
    if not validate_input(location=location):
        return put_ship(
            player=player,
            ship=ship,
            message=error_input.format(
                location,
                chr(ord('a') + BOARD_SIZE - 1),
                BOARD_SIZE))
    ship.col_idx, ship.row_idx = get_idx_from_location(location)
    ship.orientation = input('Is it horizontal or vertical? (H)/V '
                             ).lower().strip()
    if not validate_ship_fit(
            ship=ship,
            board=player.self_board.board):
        return put_ship(
            player=player,
            ship=ship,
            message=error_fit.format(location))
    if not validate_ship_overlap(
            ship=ship,
            board=player.self_board):
        return put_ship(
            player=player,
            ship=ship,
            message=error_overlap.format(location))
    if ship.orientation != 'v':
        marker = HORIZONTAL_SHIP
    else:
        marker = VERTICAL_SHIP
    mark_ship(
        ship=ship,
        marker=marker,
        board=player.self_board)
    ship.make_occup_list()


def put_ships(player):
    input('{}, it is time to place your ships! '
          'Press enter to continue. '.format(player.name))
    for ship in player.ships:
        put_ship(player=player, ship=ship)
        clear_and_print_one_board(board=player.self_board.board)
    input('{}, you have placed all your ships. '
          'Press enter to continue. '.format(player.name))
    clear_screen()


def mark_ship(ship, marker, board):
    """The ship is marked with a provided marker on the specified board."""
    if ship.orientation != 'v':
        index = ship.col_idx
        max_idx = ship.col_idx + ship.size
        while index < max_idx:
            board.put_value_at_place(
                col_idx=index,
                row_idx=ship.row_idx,
                value=marker)
            index += 1
    else:
        max_idx = ship.row_idx + ship.size
        index = ship.row_idx
        while index < max_idx:
            board.put_value_at_place(
                col_idx=ship.col_idx,
                row_idx=index,
                value=marker
            )
            index += 1


def validate_ship_fit(ship, board):
    """Validates whether a ship fits on the board by comparing the highest
     index with the board size."""
    if ship.orientation != 'v':
        max_idx = ship.col_idx + ship.size
    else:
        max_idx = ship.row_idx + ship.size

    if max_idx > len(board):
        return False
    return True


def validate_ship_overlap(ship, board):
    """Validates whether a ship overlaps with any previously placed ships.
    """
    if ship.orientation != 'v':
        max_idx = ship.col_idx + ship.size
        index = ship.col_idx
        while index < max_idx:
            if board.get_value_at_place(index, ship.row_idx) != EMPTY:
                return False
            index += 1
    else:
        max_idx = ship.row_idx + ship.size
        index = ship.row_idx
        while index < max_idx:
            if board.get_value_at_place(ship.col_idx, index) != EMPTY:
                return False
            index += 1
    return True


def validate_input(location):
    """Validates whether user input is valid."""
    poss_letters = "".join(
        [chr(c) for c in range(ord('a'), ord('a') + BOARD_SIZE)])
    match = r'^[{}]\d{{1,2}}$'.format(poss_letters)
    if re.match(match, location):
        row_idx = int(location[1:]) - 1
        if row_idx not in range(BOARD_SIZE):
            return False
    else:
        return False
    return True


def get_ship_from_location(player, col_idx, row_idx):
    """Returns a player's ship that occupies the provided location."""
    for ship in player.ships:
        if (row_idx, col_idx) in ship.occup:
            return ship


def sink_ship(ship, player):
    """Marks a sink as sunk at the player's guess board and at player
    opponent's board."""
    mark_ship(
        ship=ship,
        marker=SUNK,
        board=player.guess_board
    )
    mark_ship(
        ship=ship,
        marker=SUNK,
        board=player.opponent.self_board
    )
    player.opponent.ships.remove(ship)


def mark_result_of_shot(player, col_idx, row_idx, value):
    """Marks a specified location with a specified marker at the player's
     guess board and at player opponent's board."""
    player.guess_board.put_value_at_place(
        col_idx=col_idx,
        row_idx=row_idx,
        value=value)
    player.opponent.self_board.put_value_at_place(
        col_idx=col_idx,
        row_idx=row_idx,
        value=value)


def validate_shot(location, player):
    """Validates a result of a player's shot depending on a marker at the
    location."""
    col_idx, row_idx = get_idx_from_location(location)
    value = player.opponent.self_board.get_value_at_place(col_idx, row_idx)
    if value == EMPTY:
        mark_result_of_shot(
            player=player,
            col_idx=col_idx,
            row_idx=row_idx,
            value=MISS
        )
        message = '{} missed!'.format(player.name)
    elif value in [MISS, HIT, SUNK]:
        return shoot(
            player=player,
            message=error_visited.format(location)
        )
    else:
        ship = get_ship_from_location(
            player=player.opponent,
            col_idx=col_idx,
            row_idx=row_idx)
        ship.occup.remove((row_idx, col_idx))
        if len(ship.occup) == 0:
            sink_ship(ship=ship, player=player)
            message = "{} sank {}'s {}!".format(
                player.name,
                player.opponent.name,
                ship.name
            )
        else:
            mark_result_of_shot(
                player=player,
                col_idx=col_idx,
                row_idx=row_idx,
                value=HIT
            )
            message = "{} hit {}'s ship!".format(
                player.name,
                player.opponent.name
            )
    return message


def shoot(player, message=None):
    """Gets a location, where a player shoots, validates a result of the
    shot and returns a corresponding message."""
    clear_and_print_two_boards(
        board1=player.self_board.board,
        board2=player.guess_board.board
    )
    if message:
        print(message)
    location = ''.join(input('{}, select a location to shoot at: '.format(
        player.name)).lower().strip().split())
    if not validate_input(location=location):
        return shoot(
            player=player,
            message=error_input.format(
                location,
                chr(ord('a') + BOARD_SIZE - 1),
                BOARD_SIZE
            )
        )
    return validate_shot(location=location, player=player)


def create_players():
    print('Player 1')
    player1 = Player()
    clear_screen()
    print('Player 2')
    player2 = Player()
    while True:
        if player2.name == player1.name:
            player2.get_name(message="Names of the players should be different!")
        else:
            break
    player1.opponent = player2
    player2.opponent = player1
    return [player1, player2]


def game():
    clear_screen()
    # Players are created.
    players = create_players()
    clear_screen()
    # Players place their ships.
    for player in players:
        put_ships(player=player)
    input("The Battle begins! {} is the first to shoot. "
          "Press enter to continue.".format(players[0].name))
    clear_screen()
    # Players take turns.
    step = 0
    while True:
        for player in players:
            if step > 0:
                input("{}, it is your turn! Press enter to continue. ".format(
                    player.name))
            step += 1
            message = shoot(player)
            if len(player.opponent.ships) == 0:
                clear_and_print_two_boards(
                    board1=player.self_board.board,
                    board2=player.guess_board.board
                )
                print(message)
                input(
                    '{} wins with only {} missiles launched! '
                    'Press enter to exit the game. '.format(
                        player.name,
                        int((step + 1) / 2)
                    )
                )
                exit()
            else:
                clear_screen()
                print(message)


if __name__ == '__main__':
    game()
