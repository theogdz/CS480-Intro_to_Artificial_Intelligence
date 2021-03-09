from search import *
from utils import *


def best_first_tree_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            frontier.append(child)
            if f(child) < frontier[child]:
                del frontier[child]
                frontier.append(child)
    return None


def uniform_cost_tree_search(problem, display=False):
    return best_first_tree_search(problem, lambda node: node.path_cost, display)


def astar_tree_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first_tree_search(problem, lambda n: n.path_cost + h(n), display)