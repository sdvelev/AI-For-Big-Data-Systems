import pytest
from utils import expr_handle_infix_ops, count, Symbol

from def_agents import *
from def_prop_logic import *

# ______________________________________________________________________________

# Description of sample propositional knowledge bases


def test_PropKB():
    kb = PropKB()
    count(kb.ask(expr) for expr in [A, C, D, E, Q]) is 0
    kb.tell(A & E)
    kb.ask(A) == kb.ask(E) == {}
    kb.tell(E |'==>'| C)
    kb.ask(C) == {}
    kb.retract(E)
    kb.ask(E) is False
    kb.ask(C) is False


class PropDefiniteKB(PropKB):
    """A KB of propositional definite clauses."""

    def tell(self, sentence):
        """Add a definite clause to this KB."""
        assert is_definite_clause(sentence), "Must be definite clause"
        self.clauses.append(sentence)

    def ask_generator(self, query):
        """Yield the empty substitution if KB implies query; else nothing."""
        if pl_fc_entails(self.clauses, query):
            yield {}

    def retract(self, sentence):
        self.clauses.remove(sentence)

    def clauses_with_premise(self, p):
        """Return a list of the clauses in KB that have p in their premise.
        This could be cached away for O(1) speed, but we'll recompute it."""
        return [c for c in self.clauses
                if c.op == '==>' and p in conjuncts(c.args[0])]

"""
Defining a sample Horn Clause knowledge base for testing the forward chaining example
"""
horn_clauses_KB = PropDefiniteKB()
for s in "P==>Q; (L&M)==>P; (B&L)==>M; (A&P)==>L; (A&B)==>L; A;B".split(';'):
    horn_clauses_KB.tell(expr(s))