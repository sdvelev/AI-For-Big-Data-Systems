from def_prop_logic import *

# Defining Logical Agent for the Wumpus World
#

# ______________________________________________________________________________
# Walk-SAT


def WalkSAT(clauses, p=0.5, max_flips=10000):
    """Checks for satisfiability of all clauses by randomly flipping values of variables
    """
    # Set of all symbols in all clauses
    symbols = {sym for clause in clauses for sym in prop_symbols(clause)}
    # model is a random assignment of true/false to the symbols in clauses
    model = {s: random.choice([True, False]) for s in symbols}
    for i in range(max_flips):
        satisfied, unsatisfied = [], []
        for clause in clauses:
            (satisfied if pl_true(clause, model) else unsatisfied).append(clause)
        if not unsatisfied:  # if model satisfies all the clauses
            return model
        clause = random.choice(unsatisfied)
        if probability(p):
            sym = random.choice(list(prop_symbols(clause)))
        else:
            # Flip the symbol in clause that maximizes number of sat. clauses
            def sat_count(sym):
                # Return the number of clauses satisfied after flipping the symbol.
                model[sym] = not model[sym]
                count = len([clause for clause in clauses if pl_true(clause, model)])
                model[sym] = not model[sym]
                return count
            sym = argmax(prop_symbols(clause), key=sat_count)
        model[sym] = not model[sym]
    # If no solution is found within the flip limit, we return failure
    return None

# ______________________________________________________________________________


class HybridWumpusAgent(Agent):
    """An agent for the wumpus world that does logical inference."""

    def __init__(self):
        raise NotImplementedError


def plan_route(current, goals, allowed):
    raise NotImplementedError

# ______________________________________________________________________________


def SAT_plan(init, transition, goal, t_max, SAT_solver=dpll_satisfiable):
    """Converts a planning problem to Satisfaction problem by translating it to a cnf sentence.
    """

    # Functions used by SAT_plan
    def translate_to_SAT(init, transition, goal, time):
        clauses = []
        states = [state for state in transition]

        # Symbol claiming state s at time t
        state_counter = itertools.count()
        for s in states:
            for t in range(time+1):
                state_sym[s, t] = Expr("State_{}".format(next(state_counter)))

        # Add initial state axiom
        clauses.append(state_sym[init, 0])

        # Add goal state axiom
        clauses.append(state_sym[goal, time])

        # All possible transitions
        transition_counter = itertools.count()
        for s in states:
            for action in transition[s]:
                s_ = transition[s][action]
                for t in range(time):
                    # Action 'action' taken from state 's' at time 't' to reach 's_'
                    action_sym[s, action, t] = Expr(
                        "Transition_{}".format(next(transition_counter)))

                    # Change the state from s to s_
                    clauses.append(action_sym[s, action, t] |'==>'| state_sym[s, t])
                    clauses.append(action_sym[s, action, t] |'==>'| state_sym[s_, t + 1])

        # Allow only one state at any time
        for t in range(time+1):
            # must be a state at any time
            clauses.append(associate('|', [state_sym[s, t] for s in states]))

            for s in states:
                for s_ in states[states.index(s) + 1:]:
                    # for each pair of states s, s_ only one is possible at time t
                    clauses.append((~state_sym[s, t]) | (~state_sym[s_, t]))

        # Restrict to one transition per timestep
        for t in range(time):
            # list of possible transitions at time t
            transitions_t = [tr for tr in action_sym if tr[2] == t]

            # make sure at least one of the transitions happens
            clauses.append(associate('|', [action_sym[tr] for tr in transitions_t]))

            for tr in transitions_t:
                for tr_ in transitions_t[transitions_t.index(tr) + 1:]:
                    # there cannot be two transitions tr and tr_ at time t
                    clauses.append(~action_sym[tr] | ~action_sym[tr_])

        # Combine the clauses to form the cnf
        return associate('&', clauses)

    def extract_solution(model):
        true_transitions = [t for t in action_sym if model[action_sym[t]]]
        # Sort transitions based on time, which is the 3rd element of the tuple
        true_transitions.sort(key=lambda x: x[2])
        return [action for s, action, time in true_transitions]

    # Body of SAT_plan algorithm
    for t in range(t_max):
        # dictionaries to help extract the solution from model
        state_sym = {}
        action_sym = {}

        cnf = translate_to_SAT(init, transition, goal, t)
        model = SAT_solver(cnf)
        if model is not False:
            return extract_solution(model)
    return None



# A simple KB that defines the relevant conditions of the Wumpus World.


wumpus_kb = PropKB()

P11, P12, P21, P22, P31, B11, B21 = expr('P11, P12, P21, P22, P31, B11, B21')
wumpus_kb.tell(~P11)
wumpus_kb.tell(B11 | '<=>' | ((P12 | P21)))
wumpus_kb.tell(B21 | '<=>' | ((P11 | P22 | P31)))
wumpus_kb.tell(~B11)
wumpus_kb.tell(B21)