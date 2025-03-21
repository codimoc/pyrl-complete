from . import rules
from .rules import Paths


def clear():
    rules.paths = []


def paths() -> Paths:
    return rules.paths


# TODO: create a bespoke parse that wraps yacc and manages its paths
