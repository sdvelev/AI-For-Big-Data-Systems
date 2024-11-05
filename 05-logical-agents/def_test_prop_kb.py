import pytest
from utils import expr_handle_infix_ops, count, Symbol

from def_agents import *
from def_prop_logic import *
from def_prop_kb import *


def test_is_symbol():
    print(is_symbol('x'))
    print(is_symbol('X'))
    print(is_symbol('N245'))
    print(not is_symbol(''))
    print(not is_symbol('1L'))
    print(not is_symbol([1, 2, 3]))


def test_is_prop_symbol():
    print(not is_prop_symbol('xt'))
    print(is_prop_symbol('Txt'))
    print(not is_prop_symbol(''))
    print(not is_prop_symbol('52'))


def test_expr():
    print(repr(expr('P <=> Q(1)')) == '(P <=> Q(1))')
    print(repr(expr('P & Q | ~R(x, F(x))')) == '((P & Q) | ~R(x, F(x)))')
    print(expr_handle_infix_ops('P & Q ==> R & ~S')
          == "P & Q |'==>'| R & ~S")


def test_pl_true():
    pl_true(P, {}) is None
    pl_true(P, {P: False}) is False
    pl_true(P | Q, {P: True}) is True
    pl_true((A | B) & (C | D), {A: False, B: True, D: True}) is True
    pl_true((A & B) & (C | D), {A: False, B: True, D: True}) is False
    pl_true((A & B) | (A & C), {A: False, B: True, C: True}) is False
    pl_true((A | B) & (C | D), {A: True, D: False}) is None
    pl_true(P | P, {}) is None


def test_tt_true():
    tt_true(P | ~P)
    tt_true('~~P <=> P')
    not tt_true((P | ~Q) & (~P | Q))
    not tt_true(P & ~P)
    not tt_true(P & Q)
    tt_true((P | ~Q) | (~P | Q))
    tt_true('(A & B) ==> (A | B)')
    tt_true('((A & B) & C) <=> (A & (B & C))')
    tt_true('((A | B) | C) <=> (A | (B | C))')
    tt_true('(A ==> B) <=> (~B ==> ~A)')
    tt_true('(A ==> B) <=> (~A | B)')
    tt_true('(A <=> B) <=> ((A ==> B) & (B ==> A))')
    tt_true('~(A & B) <=> (~A | ~B)')
    tt_true('~(A | B) <=> (~A & ~B)')
    tt_true('(A & (B | C)) <=> ((A & B) | (A & C))')
    tt_true('(A | (B & C)) <=> ((A | B) & (A | C))')


def test_find_pure_symbol():
    find_pure_symbol([A, B, C], [A | ~B, ~B | ~C, C | A]) == (A, True)
    find_pure_symbol([A, B, C], [~A | ~B, ~B | ~C, C | A]) == (B, False)
    find_pure_symbol([A, B, C], [~A | B, ~B | ~C, C | A]) == (None, None)


def test_unit_clause_assign():
    unit_clause_assign(A | B | C, {A: True}) == (None, None)
    unit_clause_assign(B | C, {A: True}) == (None, None)
    unit_clause_assign(B | ~A, {A: True}) == (B, True)


def test_find_unit_clause():
    find_unit_clause([A | B | C, B | ~C, ~A | ~B], {A: True}) == (B, False)


def test_pl_fc_entails():
    pl_fc_entails(horn_clauses_KB, expr('Q'))
    not pl_fc_entails(horn_clauses_KB, expr('SomethingSilly'))


def test_tt_entails():
    tt_entails(P & Q, Q)
    not tt_entails(P | Q, Q)
    tt_entails(A & (B | C) & E & F & ~(P | Q), A & E & F & ~P & ~Q)


def test_eliminate_implications():
    repr(eliminate_implications('A ==> (~B <== C)')) == '((~B | ~C) | ~A)'
    repr(eliminate_implications(A ^ B)) == '((A & ~B) | (~A & B))'
    repr(eliminate_implications(A & B | C & ~D)) == '((A & B) | (C & ~D))'


def test_dissociate():
    dissociate('&', [A & B]) == [A, B]
    dissociate('|', [A, B, C & D, P | Q]) == [A, B, C & D, P, Q]
    dissociate('&', [A, B, C & D, P | Q]) == [A, B, C, D, P | Q]


def test_associate():
    (repr(associate('&', [(A & B), (B | C), (B & C)]))
     == '(A & B & (B | C) & B & C)')
    (repr(associate('|', [A | (B | (C | (A & B)))]))
     == '(A | B | C | (A & B))')


def test_move_not_inwards():
    repr(move_not_inwards(~(A | B))) == '(~A & ~B)'
    repr(move_not_inwards(~(A & B))) == '(~A | ~B)'
    repr(move_not_inwards(~(~(A | ~B) | ~~C))) == '((A | ~B) & ~C)'


def test_distribute_and_over_or():
    def test_enatilment(s, has_and=False):
        result = distribute_and_over_or(s)
        if has_and:
            result.op == '&'
        tt_entails(s, result)
        tt_entails(result, s)

    test_enatilment((A & B) | C, True)
    test_enatilment((A | B) & C, True)
    test_enatilment((A | B) | C, False)
    test_enatilment((A & B) | (C | D), True)


def test_to_cnf():
    repr(to_cnf((P & Q) | (~P & ~Q))) == '((~P | P) & (~Q | P) & (~P | Q) & (~Q | Q))'
    repr(to_cnf("B <=> (P1 | P2)")) == '((~P1 | B) & (~P2 | B) & (P1 | P2 | ~B))'
    repr(to_cnf("a | (b & c) | d")) == '((b | a | d) & (c | a | d))'
    repr(to_cnf("A & (B | (D & E))")) == '(A & (D | B) & (E | B))'
    repr(to_cnf("A | (B | (C | (D & E)))")) == '((D | A | B | C) & (E | A | B | C))'