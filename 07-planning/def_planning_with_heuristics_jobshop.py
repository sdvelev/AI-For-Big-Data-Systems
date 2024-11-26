"""Planning with heuristics example (Chapter 10)
"""

from def_planning_with_heuristics import *


def job_shop_problem():
    """
    [figure 11.1] JOB-SHOP-PROBLEM

    A job-shop scheduling problem for assembling two cars,
    with resource and ordering constraints.

    Example:
    >>> from def_planning import *
    >>> from def_planning_and_acting import *
    >>> p = job_shop_problem()
    >>> p.goal_test()
    False
    >>> p.act(p.jobs[1][0])
    >>> p.act(p.jobs[1][1])
    >>> p.act(p.jobs[1][2])
    >>> p.act(p.jobs[0][0])
    >>> p.act(p.jobs[0][1])
    >>> p.goal_test()
    False
    >>> p.act(p.jobs[0][2])
    >>> p.goal_test()
    True
    >>>
    """
    init = [expr('Car(C1)'),
            expr('Car(C2)'),
            expr('Wheels(W1)'),
            expr('Wheels(W2)'),
            expr('Engine(E2)'),
            expr('Engine(E2)')]

    def goal_test(kb):
        # print(kb.clauses)
        required = [expr('Has(C1, W1)'), expr('Has(C1, E1)'), expr('Inspected(C1)'),
                    expr('Has(C2, W2)'), expr('Has(C2, E2)'), expr('Inspected(C2)')]
        for q in required:
            # print(q)
            # print(kb.ask(q))
            if kb.ask(q) is False:
                return False
        return True

    resources = {'EngineHoists': 1, 'WheelStations': 2, 'Inspectors': 2, 'LugNuts': 500}

    # AddEngine1
    precond_pos = []
    precond_neg = [expr("Has(C1,E1)")]
    effect_add = [expr("Has(C1,E1)")]
    effect_rem = []
    add_engine1 = HLA(expr("AddEngine1"),
                      [precond_pos, precond_neg], [effect_add, effect_rem],
                      duration=30, use={'EngineHoists': 1})

    # AddEngine2
    precond_pos = []
    precond_neg = [expr("Has(C2,E2)")]
    effect_add = [expr("Has(C2,E2)")]
    effect_rem = []
    add_engine2 = HLA(expr("AddEngine2"),
                      [precond_pos, precond_neg], [effect_add, effect_rem],
                      duration=60, use={'EngineHoists': 1})

    # AddWheels1
    precond_pos = []
    precond_neg = [expr("Has(C1,W1)")]
    effect_add = [expr("Has(C1,W1)")]
    effect_rem = []
    add_wheels1 = HLA(expr("AddWheels1"),
                      [precond_pos, precond_neg], [effect_add, effect_rem],
                      duration=30, consume={'LugNuts': 20}, use={'WheelStations': 1})

    # AddWheels2
    precond_pos = []
    precond_neg = [expr("Has(C2,W2)")]
    effect_add = [expr("Has(C2,W2)")]
    effect_rem = []
    add_wheels2 = HLA(expr("AddWheels2"),
                      [precond_pos, precond_neg], [effect_add, effect_rem],
                      duration=15, consume={'LugNuts': 20}, use={'WheelStations': 1})

    # Inspect1
    precond_pos = []
    precond_neg = [expr("Inspected(C1)")]
    effect_add = [expr("Inspected(C1)")]
    effect_rem = []
    inspect1 = HLA(expr("Inspect1"),
                   [precond_pos, precond_neg], [effect_add, effect_rem],
                   duration=10, use={'Inspectors': 1})

    # Inspect2
    precond_pos = []
    precond_neg = [expr("Inspected(C2)")]
    effect_add = [expr("Inspected(C2)")]
    effect_rem = []
    inspect2 = HLA(expr("Inspect2"),
                   [precond_pos, precond_neg], [effect_add, effect_rem],
                   duration=10, use={'Inspectors': 1})

    job_group1 = [add_engine1, add_wheels1, inspect1]
    job_group2 = [add_engine2, add_wheels2, inspect2]

    return Problem(init, [add_engine1, add_engine2, add_wheels1, add_wheels2, inspect1, inspect2],
                   goal_test, [job_group1, job_group2], resources)
