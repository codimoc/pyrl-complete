from typing import List, Self
from .rules import Paths


class Node:

    def __init__(self, name: str):
        self.children = {}  # name -> node map for children
        self.name = name

    @classmethod
    def populate_path(cls, parent: Self, path: List):
        "Vist the tree populating from a single path"
        # this is recursive and should complete
        # when the entire path is consumed
        if len(path) == 0:
            return  # end of recursion
        first = path[0]
        if first not in parent.children:
            parent.children[first] = Node(first)
        parent = parent.children[first]
        # now recurse to traverse the tree
        cls.populate_path(parent, path[1:])

    @classmethod
    def populate_tree(cls, parent: Self, paths: Paths):
        "Populate the entire tree from the paths"
        for p in paths:
            cls.populate_path(parent, p)
