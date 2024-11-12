import pytest
from def_FOL_logic import *
from utils import expr_handle_infix_ops, count, Symbol


def test_is_symbol():
    is_symbol('x')
    is_symbol('X')
    is_symbol('N245')
    not is_symbol('')
    not is_symbol('1L')
    not is_symbol([1, 2, 3])


def test_is_var_symbol():
    is_var_symbol('xt')
    not is_var_symbol('Txt')
    not is_var_symbol('')
    not is_var_symbol('52')


def test_is_prop_symbol():
    not is_prop_symbol('xt')
    is_prop_symbol('Txt')
    not is_prop_symbol('')
    not is_prop_symbol('52')


def test_variables():
    variables(expr('F(x, x) & G(x, y) & H(y, z) & R(A, z, 2)')) == {x, y, z}
    variables(expr('(x ==> y) & B(x, y) & A')) == {x, y}


def test_expr():
    repr(expr('P <=> Q(1)')) == '(P <=> Q(1))'
    repr(expr('P & Q | ~R(x, F(x))')) == '((P & Q) | ~R(x, F(x)))'
    (expr_handle_infix_ops('P & Q ==> R & ~S')
            == "P & Q |'==>'| R & ~S")


def test_extend():
    extend({x: 1}, y, 2) == {x: 1, y: 2}


def test_subst():
    subst({x: 42, y:0}, F(x) + y) == (F(42) + 0)


def test_find_pure_symbol():
    find_pure_symbol([A, B, C], [A|~B,~B|~C,C|A]) == (A, True)
    find_pure_symbol([A, B, C], [~A|~B,~B|~C,C|A]) == (B, False)
    find_pure_symbol([A, B, C], [~A|B,~B|~C,C|A]) == (None, None)


def test_unit_clause_assign():
    unit_clause_assign(A|B|C, {A:True}) == (None, None)
    unit_clause_assign(B|C, {A:True}) == (None, None)
    unit_clause_assign(B|~A, {A:True}) == (B, True)


def test_find_unit_clause():
    find_unit_clause([A|B|C, B|~C, ~A|~B], {A:True}) == (B, False)
    

def test_unify():
    unify(x, x, {}) == {}
    unify(x, 3, {}) == {x: 3}


def test_prop_symbols():
    prop_symbols(expr('x & y & z | A')) == {A}
    prop_symbols(expr('(x & B(z)) ==> Farmer(y) | A')) == {A, expr('Farmer(y)'), expr('B(z)')}


def test_constant_symbols():
    constant_symbols(expr('x & y & z | A')) == {A}
    constant_symbols(expr('(x & B(z)) & Father(John) ==> Farmer(y) | A')) == {A, expr('John')}


def test_predicate_symbols():
    predicate_symbols(expr('x & y & z | A')) == set()
    predicate_symbols(expr('(x & B(z)) & Father(John) ==> Farmer(y) | A')) == {
        ('B', 1),
        ('Father', 1),
        ('Farmer', 1)}
    predicate_symbols(expr('(x & B(x, y, z)) & F(G(x, y), x) ==> P(Q(R(x, y)), x, y, z)')) == {
        ('B', 3),
        ('F', 2),
        ('G', 2),
        ('P', 4),
        ('Q', 1),
        ('R', 2)}


def test_standardize_variables():
    e = expr('F(a, b, c) & G(c, A, 23)')
    len(variables(standardize_variables(e))) == 3
    # variables(e).intersection(variables(standardize_variables(e))) == {}
    is_variable(standardize_variables(expr('x')))


