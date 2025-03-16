from . import rules
from .rules import Paths

def clear():
    rules.paths = []

def paths() -> Paths:
    return rules.paths