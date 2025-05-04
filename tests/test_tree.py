from pyrl_complete.parser import Node, Tree
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


def test_regexp():
    root = Node("root", None)
    paths: Paths = [["one", "two", "three"]]
    Node.populate_tree(root, paths)
    assert root.regexp() == "^$", "root regexp"
    assert root.children["one"].regexp() == "^.*one$"
    regexp = root.children["one"].children["two"].regexp()
    assert regexp == "^.*one\\s+two$"
    regexp = root.children["one"].children["two"].children["three"].regexp()
    assert regexp == "^.*one\\s+two\\s+three$"


def test_matches():
    root = Node("root", None)
    paths: Paths = [["one", "two", "three"]]
    Node.populate_tree(root, paths)
    assert root.matches("")
    assert root.children["one"].matches("one")
    assert root.children["one"].children["two"].matches("one two")
    assert (
        root.children["one"].children["two"].children["three"].matches("one two three")
    )
    # Test non-matching cases
    assert not root.children["one"].matches("on")
    assert not root.children["one"].children["two"].matches("one tw")
    assert not root.children["one"].children["two"].matches("one two three")


def test_suggestions():
    """Tests the suggestions method of a Node."""
    root = Node("root", None)
    paths: Paths = [
        ["one", "two"],
        ["one", "three"],
        ["four"],
    ]
    Node.populate_tree(root, paths)

    # Suggestions from root
    root_suggestions = root.suggestions()
    assert len(root_suggestions) == 2
    assert "one" in root_suggestions
    assert "four" in root_suggestions

    # Suggestions from node "one"
    one_suggestions = root.children["one"].suggestions()
    assert len(one_suggestions) == 2
    assert "two" in one_suggestions
    assert "three" in one_suggestions

    # Suggestions from leaf node "two"
    assert root.children["one"].children["two"].suggestions() == []
    # Suggestions from leaf node "four"
    assert root.children["four"].suggestions() == []


def test_tree_creation_and_find_node():
    """Tests Tree instantiation and the find_node method."""
    root = Node("root", None)
    paths: Paths = [["get", "file"], ["get", "status"], ["set", "value"]]
    Node.populate_tree(root, paths)
    tree = Tree(root)

    assert tree.root is root
    assert tree.cache == {}

    # Find existing nodes
    assert tree.find_node(tree.root, "get") is root.children["get"]
    assert (
        tree.find_node(tree.root, "get file") is root.children["get"].children["file"]
    )
    assert (
        tree.find_node(tree.root, "set value") is root.children["set"].children["value"]
    )

    # Find non-existing node
    assert tree.find_node(tree.root, "get stat") is None
    assert tree.find_node(tree.root, "delete") is None

    # Check cache (simple check - assumes find_node populates it)
    assert "get" in tree.cache
    assert tree.cache["get"] is root.children["get"]
    assert "get file" in tree.cache
    assert tree.cache["get file"] is root.children["get"].children["file"]
