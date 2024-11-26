"""Planning (Chapter 10)
"""

from def_planning import *





def have_cake_and_eat_cake_too():
    init = [expr('Have(Cake)')]

    def goal_test(kb):
        required = [expr('Have(Cake)'), expr('Eaten(Cake)')]
        return all(kb.ask(q) is not False for q in required)

    # Actions

    # Eat cake
    precond_pos = [expr('Have(Cake)')]
    precond_neg = []
    effect_add = [expr('Eaten(Cake)')]
    effect_rem = [expr('Have(Cake)')]
    eat_cake = Action(expr('Eat(Cake)'), [precond_pos, precond_neg], [effect_add, effect_rem])

    # Bake Cake
    precond_pos = []
    precond_neg = [expr('Have(Cake)')]
    effect_add = [expr('Have(Cake)')]
    effect_rem = []
    bake_cake = Action(expr('Bake(Cake)'), [precond_pos, precond_neg], [effect_add, effect_rem])

    return PDDL(init, [eat_cake, bake_cake], goal_test)
