import pytest
from def_search import *


romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)


def test_find_min_edge():
    assert romania_problem.find_min_edge() == 70


def test_breadth_first_tree_search():
    assert breadth_first_tree_search(
        romania_problem).solution() == ['Sibiu', 'Fagaras', 'Bucharest']


def test_breadth_first_search():
    assert breadth_first_search(romania_problem).solution() == ['Sibiu', 'Fagaras', 'Bucharest']


def test_best_first_graph_search():
    assert best_first_graph_search(
        romania_problem,
        lambda node: node.state).solution() == ['Sibiu', 'Fagaras', 'Bucharest']
    assert best_first_graph_search(
        romania_problem,
        lambda node: node.state[::-1]).solution() == ['Timisoara',
                                                      'Lugoj',
                                                      'Mehadia',
                                                      'Drobeta',
                                                      'Craiova',
                                                      'Pitesti',
                                                      'Bucharest']


def test_uniform_cost_search():
    assert uniform_cost_search(
        romania_problem).solution() == ['Sibiu', 'Rimnicu', 'Pitesti', 'Bucharest']


def test_depth_first_graph_search():
    solution = depth_first_graph_search(romania_problem).solution()
    assert solution[-1] == 'Bucharest'


def test_iterative_deepening_search():
    assert iterative_deepening_search(
        romania_problem).solution() == ['Sibiu', 'Fagaras', 'Bucharest']


def test_depth_limited_search():
    solution_3 = depth_limited_search(romania_problem, 3).solution()
    assert solution_3[-1] == 'Bucharest'
    assert depth_limited_search(romania_problem, 2) == 'cutoff'
    solution_50 = depth_limited_search(romania_problem).solution()
    assert solution_50[-1] == 'Bucharest'

if __name__ == '__main__':
    pytest.main()