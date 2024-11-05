import pytest

from utils import expr_handle_infix_ops, count, Symbol

from def_agents import *
from def_prop_logic import *
from def_wumpus_kb import *
from def_test_wumpus_kb import *

test_wumpus_kb()

test_to_cnf()

test_pl_resolution()

test_WalkSAT()