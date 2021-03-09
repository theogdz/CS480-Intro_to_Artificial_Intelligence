import sys
import numpy as np
from games import Game, GameState, alpha_beta_search

def minmax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    game.nonterminal_state += 1
    util = playgame(state,game)
    if util == 1:
        game.nonterminal_win += 1
    elif util == -1:
        game.nonterminal_loss += 1
    else:
        game.nonterminal_draw +=1
    def max_value(state):
        if game.terminal_test(state):
            game.terminal_state += 1
            if game.utility(state, player) == 1:
                game.x_state += 1
            elif game.utility(state, player) == -1:
                game.o_state += 1
            else:
                game.draw_state += 1
            return game.utility(state, player)

        game.nonterminal_state += 1
        util = playgame(state, game)
        if util == 1:
            game.nonterminal_win += 1
        elif util == -1:
            game.nonterminal_loss += 1
        else:
            game.nonterminal_draw += 1
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            game.terminal_state += 1
            if game.utility(state, player) == 1:
                game.x_state += 1
            elif game.utility(state, player) == -1:
                game.o_state += 1
            else:
                game.draw_state += 1

            return game.utility(state, player)
        game.nonterminal_state += 1
        util = playgame(state, game)
        if util == 1:
            game.nonterminal_win += 1
        elif util == -1:
            game.nonterminal_loss += 1
        else:
            game.nonterminal_draw += 1
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    terminal_state = 0
    x_state = 0
    o_state = 0
    draw_state = 0
    nonterminal_state = 0
    nonterminal_win = 0
    nonterminal_loss = 0
    nonterminal_draw = 0

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k

def playgame(state,game):
    temp = GameState(to_move=state.to_move, utility=state.utility, board=state.board.copy(), moves= state.moves.copy())
    utility = temp.utility
    possibleMove = temp.moves
    turn = temp.to_move
    alreadyMove = temp.board
    while len(possibleMove) > 0 and utility == 0:
        optimalMove = alpha_beta_search(temp, game)
        alreadyMove[optimalMove] = turn
        possibleMove.remove(optimalMove)
        utility = game.compute_utility(alreadyMove, optimalMove, turn)

        if utility == 1:
            break
        elif utility == -1:
            break
        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'
        temp = GameState(turn, utility, alreadyMove, possibleMove)

    return utility
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


    def turnMeth(xcount, ocount):
        if xcount > ocount:
            b = 'O'
        else:
            b = 'X'
        return b


    turn = turnMeth(xcount, ocount)
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
    minmax_decision(state, game)
    # Starting from this state, populate the full game tree.
    # The leaf nodes are the terminal states.
    # The terminal state is terminal if a player wins or there are no empty squares.
    # If a player wins, the state is considered terminal, even if there are still empty squares.
    # Answer the following questions for this game tree.
    print('How many terminal states are there?')
    print(game.terminal_state)
    print('In how many of those terminal states does X win?')
    # TODO print the answer
    print(game.x_state)
    print('In how many of those terminal states does X lose?')
    # TODO print the answer
    print(game.o_state)
    print('In how many of those terminal states does X draw?')
    # TODO print the answer
    print(game.draw_state)
    print('How many non-terminal states are there?')
    # TODO print the answer
    print(game.nonterminal_state)
    print('In how many of those non-terminal states does X have a guranteed win?')
    # TODO print the answer
    print(game.nonterminal_win)
    print('In how many of those non-terminal states does X have a guranteed loss?')
    # TODO print the answer
    print(game.nonterminal_loss)
    print('In how many of those non-terminal states does X have a guranteed draw?')
    print(game.nonterminal_draw)