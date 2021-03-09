# TODO import the necessary classes and methods
import sys
import search
from games import *

if __name__ == '__main__':
    board = []
    input_file = sys.argv[1]
    file = open(input_file, 'r')
    while 1:
        # read by character
        char = file.read(1)
        if not char:
            break
        if (char != '\n') and (char != ' '):
            board.append(char)
    file.close()

    xcount = board.count('X')
    ocount = board.count('O')
    # TODO implement
    print('Whose turn is it in this state?')


    # TODO: print either X or O
    #
    def turnMeth(xcount, ocount):
        if xcount > ocount:
            b = 'O'
        else:
            b = 'X'
        return b

    turn = turnMeth(xcount, ocount)
    print(turn)
    alreadyMove = {}
    possibleMove = []
    for i in range(len(board)):
        if board[i] == '-':
            possibleMove.append(((i // 3), i % 3))
        elif board[i] == 'X':
            alreadyMove[(((i // 3), i % 3))] = 'X'
        else:
            alreadyMove[(((i // 3), i % 3))] = 'O'


    # TODO: print one of win, loss, draw
    # Check if game is over
    def check_win(c):
        player_symbol = ['X', 'O']
        winning_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for check in winning_positions:
            first_symbol = c[check[0]]
            if first_symbol != ' ' and first_symbol != '-':
                won = True
                for point in check:
                    if c[point] != first_symbol:
                        won = False
                        break
                if won:
                    if first_symbol == player_symbol[0]:
                        return 1
                    else:
                        return -1
        return 0

    last = 'draw'
    utility = check_win(board)

    game = TicTacToe()
    state = GameState(turn, utility, alreadyMove, possibleMove)
    while len(possibleMove) > 0 and utility == 0:
        optimalMove = alpha_beta_search(state, game)
        alreadyMove[optimalMove] = turn
        possibleMove.remove(optimalMove)
        utility = game.compute_utility(alreadyMove, optimalMove, turn)
        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'
        state = GameState(turn, utility, alreadyMove, possibleMove)
    if utility == 1:
        last = 'win'
    elif utility == -1:
        last = 'loss'
    print('If both X and O play optimally from this state, does X have a guaranteed win, guaranteed loss, '
          'or guaranteed draw')
    print(last)