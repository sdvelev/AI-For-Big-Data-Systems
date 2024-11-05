import pytest

from utils import expr_handle_infix_ops, count, Symbol

from def_agents import *
from def_prop_logic import *
from def_wumpus_kb import *

def test_wumpus_kb():
    # Statement: There is no pit in [1,1].
    wumpus_kb.ask(~P11) == {}

    # Statement: There is no pit in [1,2].
    wumpus_kb.ask(~P12) == {}

    # Statement: There is a pit in [2,2].
    wumpus_kb.ask(P22) is False

    # Statement: There is a pit in [3,1].
    wumpus_kb.ask(P31) is False

    # Statement: Neither [1,2] nor [2,1] contains a pit.
    wumpus_kb.ask(~P12 & ~P21) == {}

    # Statement: There is a pit in either [2,2] or [3,1].
    wumpus_kb.ask(P22 | P31) == {}


"""
Simple inference in a wumpus world example
"""
wumpus_world_inference = expr("(B11 <=> (P12 | P21))  &  ~B11")


def test_to_cnf():
    (repr(to_cnf(wumpus_world_inference & ~expr('~P12'))) ==
            "((~P12 | B11) & (~P21 | B11) & (P12 | P21 | ~B11) & ~B11 & P12)")


def test_pl_resolution():
    # TODO: Add fast test cases
    pl_resolution(wumpus_kb, ~P11)


def test_WalkSAT():
    def check_SAT(clauses, single_solution={}):
        # Make sure the solution is correct if it is returned by WalkSat
        # Sometimes WalkSat may run out of flips before finding a solution
        soln = WalkSAT(clauses)
        if soln:
            all(pl_true(x, soln) for x in clauses)
            if single_solution:  # Cross check the solution if only one exists
                all(pl_true(x, single_solution) for x in clauses)
                soln == single_solution
    # Test WalkSat for problems with solution
    check_SAT([A & B, A & C])
    check_SAT([A | B, P & Q, P & B])
    check_SAT([A & B, C | D, ~(D | P)], {A: True, B: True, C: True, D: False, P: False})
    # Test WalkSat for problems without solution
    WalkSAT([A & ~A], 0.5, 100) is None
    WalkSAT([A | B, ~A, ~(B | C), C | D, P | Q], 0.5, 100) is None
    WalkSAT([A | B, B & C, C | D, D & A, P, ~P], 0.5, 100) is None