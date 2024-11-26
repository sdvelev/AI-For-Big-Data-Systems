from def_planning_with_heuristics_sparetire import *


def test_action():
    precond = [[expr("P(x)"), expr("Q(y, z)")], [expr("Q(x)")]]
    effect = [[expr("Q(x)")], [expr("P(x)")]]
    a=Action(expr("A(x,y,z)"), precond, effect)
    args = [expr("A"), expr("B"), expr("C")]
    a.substitute(expr("P(x, z, y)"), args) == expr("P(A, C, B)")
    test_kb = FolKB([expr("P(A)"), expr("Q(B, C)"), expr("R(D)")])
    a.check_precond(test_kb, args)
    a.act(test_kb, args)
    test_kb.ask(expr("P(A)")) is False
    test_kb.ask(expr("Q(A)")) is not False
    test_kb.ask(expr("Q(B, C)")) is not False
    not a.check_precond(test_kb, args)


def test_spare_tire():
    p = spare_tire()
    p.goal_test() is False
    solution = [expr("Remove(Flat, Axle)"),
                expr("Remove(Spare, Trunk)"),
                expr("PutOn(Spare, Axle)")]

    for action in solution:
        p.act(action)

    p.goal_test()




def test_graph_call():
    pddl = spare_tire()
    negkb = FolKB([expr('At(Flat, Trunk)')])
    graph = Graph(pddl, negkb)

    levels_size = len(graph.levels)
    graph()

    levels_size == len(graph.levels) - 1
