from search import *
from helper import *
import utils
import sys

class MapProblem(Problem):

    def __init__(self, initial, goal, edgeDicts, heurisitic):
        self.initial = initial
        self.goal = goal
        self.edgeDicts = edgeDicts
        self.heurisitic = heurisitic

    def actions(self, state):
        return self.edgeDicts[state].keys()

    def result(self, state, action):
        return action

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        c += int(self.edgeDicts[state1][state2])
        return c

    def value(self, state):
        return 0

    def h(self, node):
        return self.heurisitic[node.state]
        return self.heurisitic[node.state]


if __name__ == '__main__':
    input_file = sys.argv[1]
    search_algo_str = sys.argv[2]
    fp = open(input_file, "r")
    lines = fp.readlines()

    # defining the edges
    edgeDicts = {}
    j=5
    while lines[j][0] != '#':
        n = lines[j][0]
        m = lines[j][2]
        idx = lines[j].index(">")
        if lines[j][idx+3] != "\n":
            cost = int(lines[j][idx+2])*10+int(lines[j][idx+3])
        else:
            cost = int(lines[j][idx+2])
        if n not in edgeDicts.keys():
            edgeDicts[n] = {}
        edgeDicts[n][m] = cost
        if lines[j][4] == "<":  # if bidirectional
            if m not in edgeDicts.keys():
                edgeDicts[m] = {}
            edgeDicts[m][n] = cost
        j+=1

    # defining goal and start
    start = lines[j+1][0]
    goal = lines[j+1][2]
    # defining h cost
    heurisiticDict = {}
    for i in range(j + 3, len(lines)):
        letter = lines[i][0]
        if len(lines[i]) > 4:
            heurisiticDict[letter] = int(lines[i][2])*10 + int(lines[i][3])
        else:
            heurisiticDict[letter] = int(lines[i][2])

#######################################################################################################

    if search_algo_str == "DFTS":
        p = MapProblem(start, goal, edgeDicts, heurisiticDict)
        goal_node = depth_first_tree_search(p)

    if search_algo_str == "DFGS":
        p = MapProblem(start, goal, edgeDicts, heurisiticDict)
        goal_node = depth_first_graph_search(p)

    if search_algo_str == "BFTS":
        p = MapProblem(start, goal, edgeDicts, heurisiticDict)
        goal_node = breadth_first_tree_search(p)

    if search_algo_str == "BFGS":
        p = MapProblem(start, goal, edgeDicts, heurisiticDict)
        goal_node = breadth_first_graph_search(p)

    if search_algo_str == "UCTS":
        p = MapProblem(start, goal, edgeDicts, heurisiticDict)
        goal_node = uniform_cost_tree_search(p)

    if search_algo_str == "UCGS":
        p = MapProblem(start, goal, edgeDicts, heurisiticDict)
        goal_node = uniform_cost_search(p)

    if search_algo_str == "GBFTS":
        p = MapProblem(start, goal, edgeDicts, heurisiticDict)
        goal_node = best_first_tree_search(p, lambda n: p.h(n))

    if search_algo_str == "GBFGS":
        p = MapProblem(start, goal, edgeDicts, heurisiticDict)
        goal_node = best_first_graph_search(p, lambda n: p.h(n))

    if search_algo_str == "ASTS":
        p = MapProblem(start, goal, edgeDicts, heurisiticDict)
        goal_node = astar_tree_search(p)

    if search_algo_str == "ASGS":
        p = MapProblem(start, goal, edgeDicts, heurisiticDict)
        goal_node = astar_search(p)

#######################################################################################################

    # Do not change the code below.
    if goal_node is not None:
        print("Solution path ", goal_node.solution())
        print("Solution cost ", goal_node.path_cost)
    else:
        print("No solution was found.")