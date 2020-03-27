from math import fabs
from string import digits

X_CELL = 'X'
O_CELL = 'O'
EMPTY_CELL = '_'
COLUMNS_NUMBER = 3
ROWS_NUMBER = 3

NOT_FINISHED = 'Game not finished'
DRAW = 'Draw'
WINNER_X = 'X wins'
WINNER_O = 'O wins'
UNEXPECTED = 'Impossible'

finish_states = (DRAW, WINNER_O, WINNER_X)

field = [[EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
         [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
         [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL]]


def print_field():
    row_boundary_symbol = '|'
    space = ' '
    empty_string = ''
    field_separator = '---------'

    print(field_separator)
    for row in field:
        print(row_boundary_symbol + space, end=empty_string)
        print(' '.join(row), end=empty_string)
        print(space + row_boundary_symbol)
    print(field_separator)


def convert_to_matrix(values):
    game_field = []
    user_input_index = 0

    for i in range(COLUMNS_NUMBER):
        row = []

        column = 0
        while column < COLUMNS_NUMBER:
            row.append(values[user_input_index])
            user_input_index += 1
            column += 1

        game_field.append(row)

    return game_field


def is_unexpected(x, o, x_strikes, o_strikes):
    return fabs(x - o) > 1 \
           or x_strikes > 1 \
           or o_strikes > 1 \
           or x_strikes == 1 and o_strikes > 0 \
           or o_strikes == 1 and x_strikes > 0


def analyze_state(field):
    empty_spaces_number = 0
    x_strikes = 0
    o_strikes = 0
    x_numbers_in_field = 0
    o_numbers_in_field = 0

    # analyze rows
    for _row in field:
        _x_numbers_in_row = 0
        _o_numbers_in_row = 0

        for _col in _row:
            if _col == X_CELL:
                _x_numbers_in_row += 1
                x_numbers_in_field += 1
            elif _col == O_CELL:
                _o_numbers_in_row += 1
                o_numbers_in_field += 1
            elif _col == EMPTY_CELL:
                empty_spaces_number += 1  # TODO count automatically?

            if _x_numbers_in_row == COLUMNS_NUMBER:
                x_strikes += 1

            if _o_numbers_in_row == COLUMNS_NUMBER:
                o_strikes += 1

    if is_unexpected(x_numbers_in_field, o_numbers_in_field, x_strikes, o_strikes):
        return UNEXPECTED

    # analyze columns
    for _col in range(COLUMNS_NUMBER):
        _x_numbers_in_row = 0
        _o_numbers_in_row = 0

        for _row in range(ROWS_NUMBER):
            cell = field[_row][_col]

            if cell == X_CELL:
                _x_numbers_in_row += 1
            elif cell == O_CELL:
                _o_numbers_in_row += 1

            if _x_numbers_in_row == COLUMNS_NUMBER:
                x_strikes += 1

            if _o_numbers_in_row == COLUMNS_NUMBER:
                o_strikes += 1

    if is_unexpected(x_numbers_in_field, o_numbers_in_field, x_strikes, o_strikes):
        return UNEXPECTED

    # analyze diagonals
    _row = 0
    _col = COLUMNS_NUMBER - 1
    left_right_diagonal = []
    right_left_diagonal = []
    diagonals = [left_right_diagonal, right_left_diagonal]
    while _row < COLUMNS_NUMBER:
        left_right_diagonal.append(field[_row][_row])
        right_left_diagonal.append(field[_row][_col])
        _row += 1
        _col -= 1

    for diagonal in diagonals:
        _x_numbers_in_row = 0
        _o_numbers_in_row = 0

        for cell in diagonal:
            if cell == X_CELL:
                _x_numbers_in_row += 1
            elif cell == O_CELL:
                _o_numbers_in_row += 1

            if _x_numbers_in_row == COLUMNS_NUMBER:
                x_strikes += 1

            if _o_numbers_in_row == COLUMNS_NUMBER:
                o_strikes += 1

    if is_unexpected(x_numbers_in_field, o_numbers_in_field, x_strikes, o_strikes):
        return UNEXPECTED

    if x_strikes == 1:
        return WINNER_X

    if o_strikes == 1:
        return WINNER_O

    if empty_spaces_number == 0:
        return DRAW

    if empty_spaces_number > 0:
        return NOT_FINISHED


def validate_coordinate(coordinates):
    def is_two_elements():
        if len(coordinates) == 2:
            return True
        print('You should enter numbers')

    def is_valid(coordinate):
        if coordinate not in digits:
            print('You should enter numbers')
            return False

        if int(coordinate) not in range(1, COLUMNS_NUMBER + 1):
            print('Coordinates should be from 1 to 3!')
            return False

        return True

    if is_two_elements():
        col, row = coordinates

        return is_valid(col) and is_valid(row)

    return False


def play(chip, row, col):
    field[row][col] = chip


def print_state():
    if state == NOT_FINISHED:
        print('Game not finished')
    elif state == WINNER_X:
        print('X wins')
    elif state == WINNER_O:
        print('O wins')
    elif state == DRAW:
        print('Draw')
    elif state == UNEXPECTED:
        print('Impossible')


# START OF THE GAME
print_field()

state = NOT_FINISHED
is_coordinates_valid = False
is_free = False
is_finished = False

chip = X_CELL
while not is_coordinates_valid or not is_free or not is_finished:
    raw_input = input('Enter the coordinates: ').split()
    is_coordinates_valid = validate_coordinate(raw_input)

    if is_coordinates_valid:
        col, row = raw_input

        _row = abs(int(row) - ROWS_NUMBER)
        _col = int(col) - 1

        is_free = field[_row][_col] == EMPTY_CELL

        if not is_free:
            print('This cell is occupied! Choose another one!')
            continue

        play(chip, _row, _col)

        chip = X_CELL if chip == O_CELL else O_CELL

        print_field()

        state = analyze_state(field)
        is_finished = state in finish_states

print_state()

