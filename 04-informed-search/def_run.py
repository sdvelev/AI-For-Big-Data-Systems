from def_problem import *

romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)
vacuum_world = GraphProblemStochastic('State_1', ['State_7', 'State_8'], vacuum_world)
eight_puzzle = EightPuzzle((1, 2, 3, 4, 5, 7, 8, 6, 0))
eight_puzzle2 = EightPuzzle((1, 0, 6, 8, 7, 5, 4, 2), (0, 1, 2, 3, 4, 5, 6, 7, 8))

def run_find_min_edge():
    romania_problem.find_min_edge() == 70


def run_breadth_first_tree_search():
    breadth_first_tree_search(
        romania_problem).solution() == ['Sibiu', 'Fagaras', 'Bucharest']


def run_breadth_first_graph_search():
    breadth_first_graph_search(romania_problem).solution() == ['Sibiu', 'Fagaras', 'Bucharest']


def run_best_first_graph_search():
    # uniform_cost_search and astar_search test it indirectly
    best_first_graph_search(
        romania_problem,
        lambda node: node.state).solution() == ['Sibiu', 'Fagaras', 'Bucharest']
    best_first_graph_search(
        romania_problem,
        lambda node: node.state[::-1]).solution() == ['Timisoara',
                                                      'Lugoj',
                                                      'Mehadia',
                                                      'Drobeta',
                                                      'Craiova',
                                                      'Pitesti',
                                                      'Bucharest']


def run_uniform_cost_search():
    uniform_cost_search(
        romania_problem).solution() == ['Sibiu', 'Rimnicu', 'Pitesti', 'Bucharest']


def run_depth_first_graph_search():
    solution = depth_first_graph_search(romania_problem).solution()
    solution[-1] == 'Bucharest'


def run_iterative_deepening_search():
    iterative_deepening_search(
        romania_problem).solution() == ['Sibiu', 'Fagaras', 'Bucharest']


def run_depth_limited_search():
    solution_3 = depth_limited_search(romania_problem, 3).solution()
    solution_3[-1] == 'Bucharest'
    depth_limited_search(romania_problem, 2) == 'cutoff'
    solution_50 = depth_limited_search(romania_problem).solution()
    solution_50[-1] == 'Bucharest'


def run_bidirectional_search():
    bidirectional_search(romania_problem) == 418
    bidirectional_search(eight_puzzle) == 12
    bidirectional_search(EightPuzzle((1, 2, 3, 4, 5, 6, 0, 7, 8))) == 2


def run_astar_search():
    astar_search(romania_problem).solution() == ['Sibiu', 'Rimnicu', 'Pitesti', 'Bucharest']
    astar_search(eight_puzzle).solution() == ['LEFT', 'LEFT', 'UP', 'RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'UP',
                                                     'LEFT', 'DOWN', 'RIGHT', 'RIGHT']
    astar_search(EightPuzzle((1, 2, 3, 4, 5, 6, 0, 7, 8))).solution() == ['RIGHT', 'RIGHT']


def run_find_blank_square():
    eight_puzzle.find_blank_square((0, 1, 2, 3, 4, 5, 6, 7, 8)) == 0
    eight_puzzle.find_blank_square((6, 3, 5, 1, 8, 4, 2, 0, 7)) == 7
    eight_puzzle.find_blank_square((3, 4, 1, 7, 6, 0, 2, 8, 5)) == 5
    eight_puzzle.find_blank_square((1, 8, 4, 7, 2, 6, 3, 0, 5)) == 7
    eight_puzzle.find_blank_square((4, 8, 1, 6, 0, 2, 3, 5, 7)) == 4
    eight_puzzle.find_blank_square((1, 0, 6, 8, 7, 5, 4, 2, 3)) == 1
    eight_puzzle.find_blank_square((1, 2, 3, 4, 5, 6, 7, 8, 0)) == 8


def run_actions():
    eight_puzzle.actions((0, 1, 2, 3, 4, 5, 6, 7, 8)) == ['DOWN', 'RIGHT']
    eight_puzzle.actions((6, 3, 5, 1, 8, 4, 2, 0, 7)) == ['UP', 'LEFT', 'RIGHT']
    eight_puzzle.actions((3, 4, 1, 7, 6, 0, 2, 8, 5)) == ['UP', 'DOWN', 'LEFT']
    eight_puzzle.actions((1, 8, 4, 7, 2, 6, 3, 0, 5)) == ['UP', 'LEFT', 'RIGHT']
    eight_puzzle.actions((4, 8, 1, 6, 0, 2, 3, 5, 7)) == ['UP', 'DOWN', 'LEFT', 'RIGHT']
    eight_puzzle.actions((1, 0, 6, 8, 7, 5, 4, 2, 3)) == ['DOWN', 'LEFT', 'RIGHT']
    eight_puzzle.actions((1, 2, 3, 4, 5, 6, 7, 8, 0)) == ['UP', 'LEFT']


def run_result():
    eight_puzzle.result((0, 1, 2, 3, 4, 5, 6, 7, 8), 'DOWN') == (3, 1, 2, 0, 4, 5, 6, 7, 8)
    eight_puzzle.result((6, 3, 5, 1, 8, 4, 2, 0, 7), 'LEFT') == (6, 3, 5, 1, 8, 4, 0, 2, 7)
    eight_puzzle.result((3, 4, 1, 7, 6, 0, 2, 8, 5), 'UP') == (3, 4, 0, 7, 6, 1, 2, 8, 5)
    eight_puzzle.result((1, 8, 4, 7, 2, 6, 3, 0, 5), 'RIGHT') == (1, 8, 4, 7, 2, 6, 3, 5, 0)
    eight_puzzle.result((4, 8, 1, 6, 0, 2, 3, 5, 7), 'LEFT') == (4, 8, 1, 0, 6, 2, 3, 5, 7)
    eight_puzzle.result((1, 0, 6, 8, 7, 5, 4, 2, 3), 'DOWN') == (1, 7, 6, 8, 0, 5, 4, 2, 3)
    eight_puzzle.result((1, 2, 3, 4, 5, 6, 7, 8, 0), 'UP') == (1, 2, 3, 4, 5, 0, 7, 8, 6)
    eight_puzzle.result((4, 8, 1, 6, 0, 2, 3, 5, 7), 'RIGHT') == (4, 8, 1, 6, 2, 0, 3, 5, 7)


def run_goal_test():
    not eight_puzzle.goal_test((0, 1, 2, 3, 4, 5, 6, 7, 8))
    not eight_puzzle.goal_test((6, 3, 5, 1, 8, 4, 2, 0, 7))
    not eight_puzzle.goal_test((3, 4, 1, 7, 6, 0, 2, 8, 5))
    eight_puzzle.goal_test((1, 2, 3, 4, 5, 6, 7, 8, 0))
    not eight_puzzle2.goal_test((4, 8, 1, 6, 0, 2, 3, 5, 7))
    not eight_puzzle2.goal_test((3, 4, 1, 7, 6, 0, 2, 8, 5))
    not eight_puzzle2.goal_test((1, 2, 3, 4, 5, 6, 7, 8, 0))
    eight_puzzle2.goal_test((0, 1, 2, 3, 4, 5, 6, 7, 8))


def run_check_solvability():
    eight_puzzle.check_solvability((0, 1, 2, 3, 4, 5, 6, 7, 8))
    eight_puzzle.check_solvability((6, 3, 5, 1, 8, 4, 2, 0, 7))
    eight_puzzle.check_solvability((3, 4, 1, 7, 6, 0, 2, 8, 5))
    eight_puzzle.check_solvability((1, 8, 4, 7, 2, 6, 3, 0, 5))
    eight_puzzle.check_solvability((4, 8, 1, 6, 0, 2, 3, 5, 7))
    eight_puzzle.check_solvability((1, 0, 6, 8, 7, 5, 4, 2, 3))
    eight_puzzle.check_solvability((1, 2, 3, 4, 5, 6, 7, 8, 0))
    not eight_puzzle.check_solvability((1, 2, 3, 4, 5, 6, 8, 7, 0))
    not eight_puzzle.check_solvability((1, 0, 3, 2, 4, 5, 6, 7, 8))
    not eight_puzzle.check_solvability((7, 0, 2, 8, 5, 3, 6, 4, 1))


def run_recursive_best_first_search():
    recursive_best_first_search(
        romania_problem).solution() == ['Sibiu', 'Rimnicu', 'Pitesti', 'Bucharest']
    recursive_best_first_search(
        EightPuzzle((2, 4, 3, 1, 5, 6, 7, 8, 0))).solution() == [
               'UP', 'LEFT', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'RIGHT', 'DOWN']

    def manhattan(node):
        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd = 0

        for i in range(8):
            for j in range(2):
                mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

        return mhd

    recursive_best_first_search(
        EightPuzzle((2, 4, 3, 1, 5, 6, 7, 8, 0)), h=manhattan).solution() == [
               'LEFT', 'UP', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'DOWN', 'UP', 'DOWN', 'RIGHT']
