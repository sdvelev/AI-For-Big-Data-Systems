from def_planning_cakeeating import *


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



def test_have_cake_and_eat_cake_too():
    p = have_cake_and_eat_cake_too()
    p.goal_test() is False
    solution = [expr("Eat(Cake)"),
                expr("Bake(Cake)")]

    for action in solution:
        p.act(action)

    p.goal_test()

