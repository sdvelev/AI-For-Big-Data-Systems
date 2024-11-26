"""Planning with heuristics example (Chapter 10)
"""

from def_planning_with_heuristics import *


def spare_tire():
    init = [expr('Tire(Flat)'),
            expr('Tire(Spare)'),
            expr('At(Flat, Axle)'),
            expr('At(Spare, Trunk)')]

    def goal_test(kb):
        required = [expr('At(Spare, Axle)')]
        return all(kb.ask(q) is not False for q in required)

    # Actions

    # Remove
    precond_pos = [expr("At(obj, loc)")]
    precond_neg = []
    effect_add = [expr("At(obj, Ground)")]
    effect_rem = [expr("At(obj, loc)")]
    remove = Action(expr("Remove(obj, loc)"), [precond_pos, precond_neg], [effect_add, effect_rem])

    # PutOn
    precond_pos = [expr("Tire(t)"), expr("At(t, Ground)")]
    precond_neg = [expr("At(Flat, Axle)")]
    effect_add = [expr("At(t, Axle)")]
    effect_rem = [expr("At(t, Ground)")]
    put_on = Action(expr("PutOn(t, Axle)"), [precond_pos, precond_neg], [effect_add, effect_rem])

    # LeaveOvernight
    precond_pos = []
    precond_neg = []
    effect_add = []
    effect_rem = [expr("At(Spare, Ground)"), expr("At(Spare, Axle)"), expr("At(Spare, Trunk)"),
                  expr("At(Flat, Ground)"), expr("At(Flat, Axle)"), expr("At(Flat, Trunk)")]
    leave_overnight = Action(expr("LeaveOvernight"), [precond_pos, precond_neg],
                             [effect_add, effect_rem])

    return PDDL(init, [remove, put_on, leave_overnight], goal_test)


def spare_tire_graphplan():
    pddl = spare_tire()
    negkb = FolKB([expr('At(Flat, Trunk)')])
    graphplan = GraphPlan(pddl, negkb)

    def goal_test(kb, goals):
        return all(kb.ask(q) is not False for q in goals)

    # Not sure
    goals_pos = [expr('At(Spare, Axle)'), expr('At(Flat, Ground)')]
    goals_neg = []

    while True:
        if (goal_test(graphplan.graph.levels[-1].poskb, goals_pos) and
                graphplan.graph.non_mutex_goals(goals_pos+goals_neg, -1)):
            solution = graphplan.extract_solution(goals_pos, goals_neg, -1)
            if solution:
                return solution
        graphplan.graph.expand_graph()
        if len(graphplan.graph.levels)>=2 and graphplan.check_leveloff():
            return None

