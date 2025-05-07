from typing import List, Self, Optional, Dict
from .rules import Paths
import re


class Node:
    "A node in the parse tree"

    def __init__(self, name: str, parent: Optional[Self]):
        self.children: Dict[str, Node] = {}  # name -> node map for children
        self.name = name
        self.parent = parent

    def level(self) -> int:
        "Returns the level of the node in the tree"
        level = 0
        node = self
        while node.parent is not None:
            level += 1
            node = node.parent
        return level

    def expression(self) -> str:
        "Returns the expression to be matched against the input"
        if self.name == "root":
            return ""
        if self.parent.name == "root":
            return self.name
        return f"{self.parent.expression()} {self.name}"

    def matches(self, input: str) -> bool:
        exp = self.expression()
        if "?" not in exp:
            return exp.startswith(input)
        if exp.endswith("?"):
            exp += " "  # to facilitate the split
        tokens = exp.split(" ? ")
        # now remove empty tokens
        tokens = [t for t in tokens if len(t) > 0]
        # remove extra spaces in input and transform into lower case
        input = re.sub(r"\s+", " ", input.lower().strip())
        for t in tokens:
            if not t.strip().startswith(input[: len(t)]):
                return False
            # now remove the part including ? from input
            input = re.sub(rf"^{t}\s+\w+\s+", "", input)
        # input should be completely consumed by all tokens

        return True


class Tree:
    "The full parse tree represntation of the grammar"

    def __init__(self, paths: Paths):
        self.root: Node = Node("root", None)
        self.cache: Dict[str, List[Node]] = (
            {}
        )  # a map from partial string input to Node list
        self._populate_tree_from_paths(paths)

    def _populate_path(self, start_node: Node, path_segments: List[str]):
        """
        Populates a single path into the tree starting from start_node.
        """
        current_node = start_node
        for segment in path_segments:
            if segment not in current_node.children:
                current_node.children[segment] = Node(segment, current_node)
            current_node = current_node.children[segment]

    def _populate_tree_from_paths(self, paths_list: Paths):
        "Populate the entire tree from the list of paths"
        for p in paths_list:
            self._populate_path(self.root, p)

    def find_matching_nodes(self, root: Node, input: str) -> List[Node]:
        "Find a list of nodes matching the input"
        # only use the cache at the root of the tree
        if root.level() == 0 and input in self.cache:
            return self.cache[input]
        nodes = []
        if root.matches(input):
            nodes.append(root)
        for n in root.children.values():
            nodes.extend(self.find_matching_nodes(n, input))
        # only at root level
        # now filter nodes based on the depth, we only keep the deepest
        if root.level() == 0:
            self.cache[input] = nodes
        return nodes

    def get_suggestions(self, root: Node, input: str) -> List[str]:
        "Returns a list of suggestions based on the input"
        nodes = self.find_matching_nodes(root, input)
        suggestions = []
        for n in nodes:
            suggestions.append(n.expression())
        return suggestions
