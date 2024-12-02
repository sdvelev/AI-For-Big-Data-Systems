
from def_prop_logic import *
from def_FOL_logic import *
# ______________________________________________________________________________


class FolKB(KB):
    """A knowledge base consisting of first-order definite clauses.
    >>> kb0 = FolKB([expr('Farmer(Mac)'), expr('Rabbit(Pete)'),
    ...              expr('(Rabbit(r) & Farmer(f)) ==> Hates(f, r)')])
    >>> kb0.tell(expr('Rabbit(Flopsie)'))
    >>> kb0.retract(expr('Rabbit(Pete)'))
    >>> kb0.ask(expr('Hates(Mac, x)'))[x]
    Flopsie
    >>> kb0.ask(expr('Wife(Pete, x)'))
    False
    """

    def __init__(self, initial_clauses=[]):
        self.clauses = []  # inefficient: no indexing
        for clause in initial_clauses:
            self.tell(clause)

    def tell(self, sentence):
        if is_definite_clause(sentence):
            self.clauses.append(sentence)
        else:
            raise Exception("Not a definite clause: {}".format(sentence))

    def ask_generator(self, query):
        return fol_bc_ask(self, query)

    def retract(self, sentence):
        self.clauses.remove(sentence)

    def fetch_rules_for_goal(self, goal):
        return self.clauses


test_kb = FolKB(
    map(expr, ['Farmer(Mac)',
               'Rabbit(Pete)',
               'Mother(MrsMac, Mac)',
               'Mother(MrsRabbit, Pete)',
               '(Rabbit(r) & Farmer(f)) ==> Hates(f, r)',
               '(Mother(m, c)) ==> Loves(m, c)',
               '(Mother(m, r) & Rabbit(r)) ==> Rabbit(m)',
               '(Farmer(f)) ==> Human(f)',
               # Note that this order of conjuncts
               # would result in infinite recursion:
               # '(Human(h) & Mother(m, h)) ==> Human(m)'
               '(Mother(m, h) & Human(h)) ==> Human(m)'
               ]))

crime_kb = FolKB(
    map(expr, ['(American(x) & Weapon(y) & Sells(x, y, z) & Hostile(z)) ==> Criminal(x)',
               'Owns(Nono, M1)',
               'Missile(M1)',
               '(Missile(x) & Owns(Nono, x)) ==> Sells(West, x, Nono)',
               'Missile(x) ==> Weapon(x)',
               'Enemy(x, America) ==> Hostile(x)',
               'American(West)',
               'Enemy(Nono, America)'
               ]))

maze_kb = FolKB(
    map(expr, ['Path(C00, C10)',
                'Path(C10, C11)',
                'Path(C10, C20)',
                'Path(C20, C30)',
                'Path(C30, C40)',
                'Path(C40, C41)',
                'Path(C41, C42)',
                'Path(C42, C43)',
                'Path(C42, C32)',
                'Path(C43, C33)',
                'Path(C33, C32)',
                'Path(C32, C22)',
                'Path(C22, C12)',
                'Path(C11, C12)',
                'Path(C12, C02)',
                'Path(C12, C13)',
                'Path(C02, C03)',
                'Path(C13, C03)',
                'Path(C13, C14)',
                'Path(C03, C04)',
                'Path(C04, C05)',
                'Path(C04, C14)',
                'Path(C14, C15)',
                'Path(C14, C24)',
                'Path(C24, C25)',
                'Path(C05, C15)',
                'Path(C15, C25)',
                'Path(C25, C35)',
                'Path(C35, C45)',
                'Start(C00)',
                #'Path(x, y) ==> Path(y, x)',
                'Path(x, y) ==> Reachable(x, y)',
                'Reachable(x, y) & Reachable(y, z) & At(y) ==> Reachable(x, z)',
                #'PathTaken'
                'Start(x) ==> At(x)',
                'At(x) & Reachable(x, y) ==> At(y)',
                # 'At(y) & Reachable(x, y) ==> At(x)',
                'At(C45) ==> End(C45)',

                'Path(x, y) & End(y) ==> PathToEnd(x, y)',
                'Path(x, z) & PathToEnd(z) ==> PathToEnd(x, y)'

                #'PathToEnd(x, y) ==> (Path(x, y) & Reachable(y, End))',
                #'PathToEnd(x, y) ==> (Path(x, z) & PathToEnd(z, y))'
               ]))

maze_kb2 = FolKB(
    map(expr, ['Path(C00, C10)',
                'Path(C10, C11)',
                'Path(C10, C20)',
                'Path(C20, C30)',
                'Path(C30, C40)',
                'Path(C40, C41)',
                'Path(C41, C42)',
                'Path(C42, C43)',
                'Path(C42, C32)',
                'Path(C43, C33)',
                'Path(C33, C32)',
                'Path(C32, C22)',
                'Path(C22, C12)',
                'Path(C11, C12)',
                'Path(C12, C02)',
                'Path(C12, C13)',
                'Path(C02, C03)',
                'Path(C13, C03)',
                'Path(C13, C14)',
                'Path(C03, C04)',
                'Path(C04, C05)',
                'Path(C04, C14)',
                'Path(C14, C15)',
                'Path(C14, C24)',
                'Path(C24, C25)',
                'Path(C05, C15)',
                'Path(C15, C25)',
                'Path(C25, C35)',
                'Path(C35, C45)',
                'Start(C00)',
                #'Path(x, y) ==> Path(y, x)',
                # 'Path(x, y) ==> Path(x, y)',
                # 'Reachable(x, y) & Reachable(y, z) & At(y) ==> Reachable(x, z)',
                #'PathTaken'
                'Start(x) ==> At(x)',
                'At(C45) ==> End(C45)',
                'Path(x, y) & At(x) ==> At(y)',
                # 'At(y) & Reachable(x, y) ==> At(x)',


                # 'Path(x, y) & End(y) ==> PathToEnd(x, y)',
                # 'Path(x, z) & PathToEnd(z) ==> PathToEnd(x, y)'

                #'PathToEnd(x, y) ==> (Path(x, y) & Reachable(y, End))',
                #'PathToEnd(x, y) ==> (Path(x, z) & PathToEnd(z, y))'
               ]))