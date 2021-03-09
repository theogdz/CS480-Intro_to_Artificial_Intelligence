from search import *
from helper import *
import utils
import sys

class Puzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to n on a board, where one of the
    squares is a blank. A state is represented as a tuple of length n, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal, g):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)
        self.g = g

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
                The result would be a list, since there are only four possible actions
                in any given state of the environment """
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        self.g = g

        if index_blank_square % g == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < g:
            possible_actions.remove('UP')
        if index_blank_square % g == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > (g * 2) - 1:
            possible_actions.remove('DOWN')
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        self.g = g

        delta = {'UP': -g, 'DOWN': g, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


if __name__ == '__main__':
    input_file = sys.argv[1]
    search_algo_str = sys.argv[2]
    fp = open(input_file, "r")
    lines = fp.readlines()
    g = len(lines) - 3
    n = (pow(g, 2)) - 1
    a = []
    initial = []
    for i in range(3, len(lines)):
        a += lines[i].split(' ')
    for j in range(0, len(a)):
        initial.append(int(a[j]))
    goal = [k for k in range(n + 1)]

    #convert the lists to tuples
    initial = tuple(initial)
    goal = tuple(goal)

    if search_algo_str == "DFTS":
        p = Puzzle(initial, goal, g)
        goal_node = depth_first_tree_search(p)

    if search_algo_str == "DFGS":
        p = Puzzle(initial, goal, g)
        goal_node = depth_first_graph_search(p)

    if search_algo_str == "BFTS":
        p = Puzzle(initial, goal, g)
        goal_node = breadth_first_tree_search(p)

    if search_algo_str == "BFGS":
        p = Puzzle(initial, goal, g)
        goal_node = breadth_first_graph_search(p)

    if search_algo_str == "UCGS":
        p = Puzzle(initial, goal, g)
        goal_node = uniform_cost_search(p)

    if search_algo_str == "UCTS":
        p = Puzzle(initial, goal, g)
        goal_node = uniform_cost_tree_search(p)

    if search_algo_str == "GBFTS":
        p = Puzzle(initial, goal, g)
        goal_node = uniform_cost_tree_search(p)

    if search_algo_str == "GBFGS":
        p = Puzzle(initial, goal, g)
        goal_node = best_first_graph_search(p, lambda n: p.h(n))

    if search_algo_str == "ASTS":
        p = Puzzle(initial, goal, g)
        goal_node = astar_tree_search(p)

    if search_algo_str == "ASGS":
        p = Puzzle(initial, goal, g)
        goal_node = astar_search(p)

    # Do not change the code below.
    if goal_node is not None:
        print("Solution path", goal_node.solution())
        print("Solution cost", goal_node.path_cost)
    else:
        print("No solution was found.")
