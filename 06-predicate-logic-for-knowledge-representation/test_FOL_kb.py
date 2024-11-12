import pytest
from utils import expr_handle_infix_ops, count, Symbol
from def_FOL_logic import *
from def_FOL_kb import *
from def_test_FOL_KB import *




def test_fol_bc_ask():
    def test_ask(query, kb=None):
        q = expr(query)
        test_variables = variables(q)
        answers = fol_bc_ask(kb or test_kb, q)
        return sorted(
            [dict((x, v) for x, v in list(a.items()) if x in test_variables)
             for a in answers], key=repr)
    repr(test_ask('Farmer(x)')) == '[{x: Mac}]'
    repr(test_ask('Human(x)')) == '[{x: Mac}, {x: MrsMac}]'
    repr(test_ask('Rabbit(x)')) == '[{x: MrsRabbit}, {x: Pete}]'
    repr(test_ask('Criminal(x)', crime_kb)) == '[{x: West}]'


def test_fol_fc_ask():
    def test_ask(query, kb=None):
        q = expr(query)
        test_variables = variables(q)
        answers = fol_fc_ask(kb or test_kb, q)
        return sorted(
            [dict((x, v) for x, v in list(a.items()) if x in test_variables)
             for a in answers], key=repr)
    repr(test_ask('Criminal(x)', crime_kb)) == '[{x: West}]'
    repr(test_ask('Enemy(x, America)', crime_kb)) == '[{x: Nono}]'
    repr(test_ask('Farmer(x)')) == '[{x: Mac}]'
    repr(test_ask('Human(x)')) == '[{x: Mac}, {x: MrsMac}]'
    repr(test_ask('Rabbit(x)')) == '[{x: MrsRabbit}, {x: Pete}]'
