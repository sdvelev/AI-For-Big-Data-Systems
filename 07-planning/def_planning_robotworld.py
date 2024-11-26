"""Planning (Chapter 10)
"""

from def_planning import *



def three_block_tower():
    init = [expr('On(A, Table)'),
            expr('On(B, Table)'),
            expr('On(C, A)'),
            expr('Block(A)'),
            expr('Block(B)'),
            expr('Block(C)'),
            expr('Clear(B)'),
            expr('Clear(C)')]

    def goal_test(kb):
        required = [expr('On(A, B)'), expr('On(B, C)')]
        return all(kb.ask(q) is not False for q in required)

    # Actions

    #  Move
    precond_pos = [expr('On(b, x)'), expr('Clear(b)'), expr('Clear(y)'), expr('Block(b)'),
                   expr('Block(y)')]
    precond_neg = []
    effect_add = [expr('On(b, y)'), expr('Clear(x)')]
    effect_rem = [expr('On(b, x)'), expr('Clear(y)')]
    move = Action(expr('Move(b, x, y)'), [precond_pos, precond_neg], [effect_add, effect_rem])

    #  MoveToTable
    precond_pos = [expr('On(b, x)'), expr('Clear(b)'), expr('Block(b)')]
    precond_neg = []
    effect_add = [expr('On(b, Table)'), expr('Clear(x)')]
    effect_rem = [expr('On(b, x)')]
    moveToTable = Action(expr('MoveToTable(b, x)'), [precond_pos, precond_neg],
                         [effect_add, effect_rem])

    return PDDL(init, [move, moveToTable], goal_test)

