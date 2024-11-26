from def_planning_with_heuristics_jobshop import *


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



def test_job_shop_problem():
    p = job_shop_problem()
    p.goal_test() is False

    solution = [p.jobs[1][0],
                p.jobs[0][0],
                p.jobs[0][1],
                p.jobs[0][2],
                p.jobs[1][1],
                p.jobs[1][2]]

    for action in solution:
        p.act(action)

    p.goal_test()

