from def_planning import *

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


def test_refinements() :
    init = [expr('At(Home)')]
    def goal_test(kb):
        return kb.ask(expr('At(SFO)'))
        
    library = {"HLA": ["Go(Home,SFO)","Taxi(Home, SFO)"],
    "steps": [["Taxi(Home, SFO)"],[]],
    "precond_pos": [["At(Home)"],["At(Home)"]],
    "precond_neg": [[],[]],
    "effect_pos": [["At(SFO)"],["At(SFO)"]],
    "effect_neg": [["At(Home)"],["At(Home)"],]}
    # Go SFO
    precond_pos = [expr("At(Home)")]
    precond_neg = []
    effect_add = [expr("At(SFO)")]
    effect_rem = [expr("At(Home)")]
    go_SFO = HLA(expr("Go(Home,SFO)"),
                      [precond_pos, precond_neg], [effect_add, effect_rem])
    # Taxi SFO
    precond_pos = [expr("At(Home)")]
    precond_neg = []
    effect_add = [expr("At(SFO)")]
    effect_rem = [expr("At(Home)")]
    taxi_SFO = HLA(expr("Go(Home,SFO)"),
                      [precond_pos, precond_neg], [effect_add, effect_rem])
    prob = Problem(init, [go_SFO, taxi_SFO], goal_test)
    result = [i for i in Problem.refinements(go_SFO, prob, library)]
    (len(result) == 1)
    (result[0].name == "Taxi")
    (result[0].args == (expr("Home"), expr("SFO")))
