from def_search import *


romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)

print('Find_Min_Edge: ', romania_problem.find_min_edge(), '\n')
print('Breadth_First_Search: ', breadth_first_search(romania_problem).solution(),'\n')
print('Breadth_First_Tree_Search: ', breadth_first_tree_search(romania_problem).solution(),'\n')
print('Uniform_Cost_Search: ', uniform_cost_search(romania_problem).solution(),'\n')
print('Depth_First_Graph_Search', depth_first_graph_search(romania_problem).solution(),'\n')
print('Iterative_Deepening_Search :', iterative_deepening_search(romania_problem).solution(),'\n')
print('Depth_Limited_Search with level = 3 :', depth_limited_search(romania_problem, 3).solution(),'\n')
print('Depth_Limited_Search with level = 5 :', depth_limited_search(romania_problem, 5).solution(),'\n')


print('--------------------------------------------')

romania_problem1 = GraphProblem('Arad', 'Eforie', romania_map)

print('Find_Min_Edge: ', romania_problem1.find_min_edge(), '\n')
print('Breadth_First_Search: ', breadth_first_search(romania_problem1).solution(),'\n')
print('Breadth_First_Tree_Search: ', breadth_first_tree_search(romania_problem1).solution(),'\n')
print('Uniform_Cost_Search: ', uniform_cost_search(romania_problem1).solution(),'\n')
print('Depth_First_Graph_Search', depth_first_graph_search(romania_problem1).solution(),'\n')
print('Iterative_Deepening_Search :', iterative_deepening_search(romania_problem1).solution(),'\n')
print('Depth_Limited_Search with level = 6 :', depth_limited_search(romania_problem1, 6).solution(),'\n')
print('Depth_Limited_Search with level = 10 :', depth_limited_search(romania_problem1, 10).solution(),'\n')