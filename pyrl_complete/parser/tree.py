from typing import List, Self
from .rules import Paths
import re


class Node:
    "A node in the parse tree"

    def __init__(self, name: str, parent: Self):
        self.children = {}  # name -> node map for children
        self.name = name
        self.parent = parent

    @classmethod
    def populate_path(cls, parent: Self, path: List):
        "Vist the tree populating from a single path"
        # this is recursive and should complete
        # when the entire path is consumed
        if len(path) == 0:
            return  # end of recursion
        first = path[0]
        if first not in parent.children:
            parent.children[first] = Node(first, parent)
        # now recurse to traverse the tree
        cls.populate_path(parent.children[first], path[1:])

    @classmethod
    def populate_tree(cls, parent: Self, paths: Paths):
        "Populate the entire tree from the paths"
        for p in paths:
            cls.populate_path(parent, p)

    def suggestions(self) -> List[str]:
        "Returns the suggestion at for this node"
        return [n for n in self.children.keys()]

    def regexp(self) -> str:
        if self.name == "root":
            return "^$"
        name = self.name
        # TODO: substitute ? with \w+
        if self.parent.name == "root":
            return f"^.*{name}$"
        return f"{self.parent.regexp()[:-1]}\\s+{name}$"

    def matches(self, input: str) -> bool:
        return re.match(self.regexp(), input) is not None


class Tree:
    "The full parse tree represntation of the grammar"

    def __init__(self, root: Node):
        self.root = root
        self.cache = {}  # a map from partial string input to Node

    def find_node(self, node: Node, input: str) -> Node:
        if input in self.cache:
            return self.cache[input]
        if node.matches(input):
            self.cache[input] = node
            return node
        for n in node.children.values():
            node = self.find_node(n, input)
            if node is not None:
                return node
        return None
