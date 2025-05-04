from pyrl_complete.parser import Node
from pyrl_complete.parser.rules import Paths


def test_simple_tree():
    paths = [["get", "one"], ["get", "two"], ["set"]]
    root = Node("root", None)
    Node.populate_tree(root, paths)
    assert len(root.children) == 2
    assert len(root.children["get"].children) == 2
    assert root.children["get"].parent.name == "root"
    assert root.children["get"].children["one"].parent.name == "get"
    assert len(root.children["set"].children) == 0


def test_node_creation():
    """Tests the basic initialization of a Node."""
    root = Node("root", None)
    assert root.name == "root"
    assert root.parent is None
    assert root.children == {}

    child = Node("child", root)
    assert child.name == "child"
    assert child.parent is root
    assert child.children == {}


def test_populate_path():
    """Tests populating the tree with a single path."""
    root = Node("root", None)
    Node.populate_path(root, ["one", "two", "three"])
    assert "one" in root.children
    assert "two" in root.children["one"].children
    assert "three" in root.children["one"].children["two"].children
    assert root.children["one"].parent is root
    assert root.children["one"].children["two"].parent is root.children["one"]


def test_populate_tree_multiple_paths():
    """Tests populating the tree with multiple, overlapping paths."""
    root = Node("root", None)
    paths: Paths = [
        ["one", "two", "three"],
        ["one", "two", "four"],
        ["one", "five"],
        ["six", "seven"],
    ]
    Node.populate_tree(root, paths)
    assert "one" in root.children
    assert "six" in root.children
    assert "two" in root.children["one"].children
    assert "five" in root.children["one"].children
    assert "three" in root.children["one"].children["two"].children
    assert "four" in root.children["one"].children["two"].children
    assert "seven" in root.children["six"].children
    assert len(root.children) == 2
    assert len(root.children["one"].children) == 2
    assert len(root.children["one"].children["two"].children) == 2
