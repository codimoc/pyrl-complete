from . import rules
from .rules import Paths
from . import parser

# redefinition to simplify namespace
Parser = parser.Parser


def clear():
    rules.paths = []


def paths() -> Paths:
    return rules.paths
