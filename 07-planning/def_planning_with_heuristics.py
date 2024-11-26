"""Planning with heuristics (Chapter 10)
"""

from def_planning import *


class Level():
    """
    Contains the state of the planning problem
    and exhaustive list of actions which use the
    states as pre-condition.
    """

    def __init__(self, poskb, negkb):
        self.poskb = poskb
        # Current state
        self.current_state_pos = poskb.clauses
        self.current_state_neg = negkb.clauses
        # Current action to current state link
        self.current_action_links_pos = {}
        self.current_action_links_neg = {}
        # Current state to action link
        self.current_state_links_pos = {}
        self.current_state_links_neg = {}
        # Current action to next state link
        self.next_action_links = {}
        # Next state to current action link
        self.next_state_links_pos = {}
        self.next_state_links_neg = {}
        self.mutex = []

    def __call__(self, actions, objects):
        self.build(actions, objects)
        self.find_mutex()

    def find_mutex(self):
        # Inconsistent effects
        for poseff in self.next_state_links_pos:
            negeff = poseff
            if negeff in self.next_state_links_neg:
                for a in self.next_state_links_pos[poseff]:
                    for b in self.next_state_links_neg[negeff]:
                        if set([a, b]) not in self.mutex:
                            self.mutex.append(set([a, b]))

        # Interference
        for posprecond in self.current_state_links_pos:
            negeff = posprecond
            if negeff in self.next_state_links_neg:
                for a in self.current_state_links_pos[posprecond]:
                    for b in self.next_state_links_neg[negeff]:
                        if set([a, b]) not in self.mutex:
                            self.mutex.append(set([a, b]))

        for negprecond in self.current_state_links_neg:
            poseff = negprecond
            if poseff in self.next_state_links_pos:
                for a in self.next_state_links_pos[poseff]:
                    for b in self.current_state_links_neg[negprecond]:
                        if set([a, b]) not in self.mutex:
                            self.mutex.append(set([a, b]))

        # Competing needs
        for posprecond in self.current_state_links_pos:
            negprecond = posprecond
            if negprecond in self.current_state_links_neg:
                for a in self.current_state_links_pos[posprecond]:
                    for b in self.current_state_links_neg[negprecond]:
                        if set([a, b]) not in self.mutex:
                            self.mutex.append(set([a, b]))

        # Inconsistent support
        state_mutex = []
        for pair in self.mutex:
            next_state_0 = self.next_action_links[list(pair)[0]]
            if len(pair) == 2:
                next_state_1 = self.next_action_links[list(pair)[1]]
            else:
                next_state_1 = self.next_action_links[list(pair)[0]]
            if (len(next_state_0) == 1) and (len(next_state_1) == 1):
                state_mutex.append(set([next_state_0[0], next_state_1[0]]))

        self.mutex = self.mutex+state_mutex

    def build(self, actions, objects):

        # Add persistence actions for positive states
        for clause in self.current_state_pos:
            self.current_action_links_pos[Expr('Persistence', clause)] = [clause]
            self.next_action_links[Expr('Persistence', clause)] = [clause]
            self.current_state_links_pos[clause] = [Expr('Persistence', clause)]
            self.next_state_links_pos[clause] = [Expr('Persistence', clause)]

        # Add persistence actions for negative states
        for clause in self.current_state_neg:
            not_expr = Expr('not'+clause.op, clause.args)
            self.current_action_links_neg[Expr('Persistence', not_expr)] = [clause]
            self.next_action_links[Expr('Persistence', not_expr)] = [clause]
            self.current_state_links_neg[clause] = [Expr('Persistence', not_expr)]
            self.next_state_links_neg[clause] = [Expr('Persistence', not_expr)]

        for a in actions:
            num_args = len(a.args)
            possible_args = tuple(itertools.permutations(objects, num_args))

            for arg in possible_args:
                if a.check_precond(self.poskb, arg):
                    for num, symbol in enumerate(a.args):
                        if not symbol.op.islower():
                            arg = list(arg)
                            arg[num] = symbol
                            arg = tuple(arg)

                    new_action = a.substitute(Expr(a.name, *a.args), arg)
                    self.current_action_links_pos[new_action] = []
                    self.current_action_links_neg[new_action] = []

                    for clause in a.precond_pos:
                        new_clause = a.substitute(clause, arg)
                        self.current_action_links_pos[new_action].append(new_clause)
                        if new_clause in self.current_state_links_pos:
                            self.current_state_links_pos[new_clause].append(new_action)
                        else:
                            self.current_state_links_pos[new_clause] = [new_action]

                    for clause in a.precond_neg:
                        new_clause = a.substitute(clause, arg)
                        self.current_action_links_neg[new_action].append(new_clause)
                        if new_clause in self.current_state_links_neg:
                            self.current_state_links_neg[new_clause].append(new_action)
                        else:
                            self.current_state_links_neg[new_clause] = [new_action]

                    self.next_action_links[new_action] = []
                    for clause in a.effect_add:
                        new_clause = a.substitute(clause, arg)
                        self.next_action_links[new_action].append(new_clause)
                        if new_clause in self.next_state_links_pos:
                            self.next_state_links_pos[new_clause].append(new_action)
                        else:
                            self.next_state_links_pos[new_clause] = [new_action]

                    for clause in a.effect_rem:
                        new_clause = a.substitute(clause, arg)
                        self.next_action_links[new_action].append(new_clause)
                        if new_clause in self.next_state_links_neg:
                            self.next_state_links_neg[new_clause].append(new_action)
                        else:
                            self.next_state_links_neg[new_clause] = [new_action]

    def perform_actions(self):
        new_kb_pos = FolKB(list(set(self.next_state_links_pos.keys())))
        new_kb_neg = FolKB(list(set(self.next_state_links_neg.keys())))

        return Level(new_kb_pos, new_kb_neg)


class Graph:
    """
    Contains levels of state and actions
    Used in graph planning algorithm to extract a solution
    """

    def __init__(self, pddl, negkb):
        self.pddl = pddl
        self.levels = [Level(pddl.kb, negkb)]
        self.objects = set(arg for clause in pddl.kb.clauses + negkb.clauses for arg in clause.args)

    def __call__(self):
        self.expand_graph()

    def expand_graph(self):
        last_level = self.levels[-1]
        last_level(self.pddl.actions, self.objects)
        self.levels.append(last_level.perform_actions())

    def non_mutex_goals(self, goals, index):
        goal_perm = itertools.combinations(goals, 2)
        for g in goal_perm:
            if set(g) in self.levels[index].mutex:
                return False
        return True


class GraphPlan:
    """
    Class for formulation GraphPlan algorithm
    Constructs a graph of state and action space
    Returns solution for the planning problem
    """

    def __init__(self, pddl, negkb):
        self.graph = Graph(pddl, negkb)
        self.nogoods = []
        self.solution = []

    def check_leveloff(self):
        first_check = (set(self.graph.levels[-1].current_state_pos) ==
                       set(self.graph.levels[-2].current_state_pos))
        second_check = (set(self.graph.levels[-1].current_state_neg) ==
                        set(self.graph.levels[-2].current_state_neg))

        if first_check and second_check:
            return True

    def extract_solution(self, goals_pos, goals_neg, index):
        level = self.graph.levels[index]
        if not self.graph.non_mutex_goals(goals_pos+goals_neg, index):
            self.nogoods.append((level, goals_pos, goals_neg))
            return

        level = self.graph.levels[index-1]

        # Create all combinations of actions that satisfy the goal
        actions = []
        for goal in goals_pos:
            actions.append(level.next_state_links_pos[goal])

        for goal in goals_neg:
            actions.append(level.next_state_links_neg[goal])

        all_actions = list(itertools.product(*actions))

        # Filter out the action combinations which contain mutexes
        non_mutex_actions = []
        for action_tuple in all_actions:
            action_pairs = itertools.combinations(list(set(action_tuple)), 2)
            non_mutex_actions.append(list(set(action_tuple)))
            for pair in action_pairs:
                if set(pair) in level.mutex:
                    non_mutex_actions.pop(-1)
                    break

        # Recursion
        for action_list in non_mutex_actions:
            if [action_list, index] not in self.solution:
                self.solution.append([action_list, index])

                new_goals_pos = []
                new_goals_neg = []
                for act in set(action_list):
                    if act in level.current_action_links_pos:
                        new_goals_pos = new_goals_pos + level.current_action_links_pos[act]

                for act in set(action_list):
                    if act in level.current_action_links_neg:
                        new_goals_neg = new_goals_neg + level.current_action_links_neg[act]

                if abs(index)+1 == len(self.graph.levels):
                    return
                elif (level, new_goals_pos, new_goals_neg) in self.nogoods:
                    return
                else:
                    self.extract_solution(new_goals_pos, new_goals_neg, index-1)

        # Level-Order multiple solutions
        solution = []
        for item in self.solution:
            if item[1] == -1:
                solution.append([])
                solution[-1].append(item[0])
            else:
                solution[-1].append(item[0])

        for num, item in enumerate(solution):
            item.reverse()
            solution[num] = item

        return solution

