from pyrl_complete.parser import Node, Tree
from pyrl_complete.parser.rules import Paths


def test_simple_tree():
    paths = [["get", "one"], ["get", "two"], ["set"]]
    tree = Tree(paths)
    root = tree.root
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


def test_populate_tree_multiple_paths():
    """Tests populating the tree with multiple, overlapping paths."""
    paths: Paths = [
        ["one", "two", "three"],
        ["one", "two", "four"],
        ["one", "five"],
        ["six", "seven"],
    ]
    tree = Tree(paths)
    root = tree.root
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


def test_matches():
    paths: Paths = [["one", "two", "three"]]
    tree = Tree(paths)
    root = tree.root
    assert root.matches("")
    node_one = root.children["one"]
    node_two = node_one.children["two"]
    node_three = node_two.children["three"]

    assert node_one.matches("one"), "matching one"
    assert node_one.matches("on"), "partial matching one"
    assert node_two.matches("one two"), "matching one two"
    assert node_two.matches("one tw"), "partial matching one two"
    assert node_three.matches("one two three"), "matching one two three"
    assert not root.children["one"].children["two"].matches("one two three")


def test_matches_complex_placeholder():
    """Test matching with a placeholder not at the end."""
    paths: Paths = [["one", "three", "five ?", "six"]]
    tree = Tree(paths)
    root = tree.root

    node_one = root.children["one"]
    node_three = node_one.children["three"]
    node_five = node_three.children["five ?"]
    node_six = node_five.children["six"]

    # Expected expression: " one three five ? six"
    assert node_six.expression() == "one three five ? six"

    # Test matching against node 'six'
    assert node_one.matches("o")  # Partial match of first segment
    assert not node_one.matches("one t")
    assert node_six.matches("one three five val1 six")
    # Test extra spaces in input
    assert node_six.matches("one  three   five 123   six")
    # Partial match of last segment.
    # Note: this is not ideal, but it is the current behavior
    # and we are testing it
    assert node_six.matches("one three five val1 si")
    assert not node_six.matches("one three five val1")  # Missing last
    assert not node_six.matches("one three five")  # Missing placeholder
    assert not node_six.matches("one three five val1 seven")  # Wrong last
    assert node_six.matches("one three five val1 six extra")  # Extra


def test_matches_multiple_placeholders():
    """Test matching with multiple placeholders."""
    paths: Paths = [["cmd", "arg1 ?", "arg2 ?", "end"]]
    tree = Tree(paths)
    root = tree.root

    node_cmd = root.children["cmd"]
    node_arg1 = node_cmd.children["arg1 ?"]
    node_arg2 = node_arg1.children["arg2 ?"]
    node_end = node_arg2.children["end"]

    # Expression: "cmd arg1 ? arg2 ? end"
    assert node_end.expression() == "cmd arg1 ? arg2 ? end"

    # Valid matches
    assert node_end.matches("cmd arg1 val1 arg2 val2 end"), "basic match"
    assert node_end.matches("cmd arg1 1 arg2 2 end"), "numeric args match"
    assert node_end.matches("cmd arg1 value_1 arg2 value_2 en"
                            ), "partial end match"
    assert node_end.matches("cmd arg1 VALUE1 arg2 VALUE2 END"
                            ), "case-insensitive match"
    assert node_end.matches(" cmd   arg1  val1  arg2 val2   end "
                            ), "extra spaces match"


def test_matches_multiple_placeholders_with_optiomn_hyphen():
    """Test matching with multiple placeholders, with an option hyphen (-)"""
    paths: Paths = [["secret_wallet", "get", "-d ?", "-a ?", "end"]]
    tree = Tree(paths)
    root = tree.root
    node_secret_wallet = root.children["secret_wallet"]
    node_get = node_secret_wallet.children["get"]
    node_arg1 = node_get.children["-d ?"]
    node_arg2 = node_arg1.children["-a ?"]
    assert node_arg2.expression() == "secret_wallet get -d ? -a ?"
    assert node_arg2.matches("secret_wallet get -d val1 -a val2")
    assert node_arg2.matches("secret_wallet get -d val1 -a ")
    # the following does not match because the end space is ignored
    assert not node_arg2.matches("secret_wallet get -d val1 ")
    assert node_arg1.matches("secret_wallet get -d val1 ")


    



def test_node_level():
    """Tests the level method of a Node."""
    paths: Paths = [
        ["one", "two", "three"],
        ["one", "four"],
    ]
    tree = Tree(paths)
    root = tree.root

    node_one = root.children["one"]
    node_two = node_one.children["two"]
    node_three = node_two.children["three"]
    node_four = node_one.children["four"]

    assert root.level() == 0
    assert node_one.level() == 1
    assert node_two.level() == 2
    assert node_three.level() == 3
    assert node_four.level() == 2


def test_node_expression():
    """Tests the expression method of a Node."""
    paths: Paths = [
        ["cmd", "sub", "arg"],
        ["other"],
    ]
    tree = Tree(paths)
    root = tree.root

    node_cmd = root.children["cmd"]
    node_sub = node_cmd.children["sub"]
    node_arg = node_sub.children["arg"]
    node_other = root.children["other"]

    assert root.expression() == "", "Root expression should be empty"
    assert node_cmd.expression() == "cmd", "First level expression"
    assert node_sub.expression() == "cmd sub", "Second level expression"
    assert node_arg.expression() == "cmd sub arg", "Third level expression"
    assert node_other.expression() == "other", "Another first level expression"


# --- Tests for Tree class ---


def test_tree_init():
    """Tests the initialization of a Tree, including root creation
    and population."""
    paths: Paths = [["cmd1", "sub1"], ["cmd2"]]
    tree = Tree(paths)

    assert tree.root is not None
    assert tree.root.name == "root"
    assert tree.root.parent is None
    assert tree.cache == {}

    # Check if tree is populated correctly
    assert "cmd1" in tree.root.children
    assert "cmd2" in tree.root.children
    assert "sub1" in tree.root.children["cmd1"].children
    assert tree.root.children["cmd1"].parent is tree.root
    assert (
        tree.root.children["cmd1"].children["sub1"].parent
        is tree.root.children["cmd1"]
    )


def test_tree_find_matching_nodes_simple():
    """Tests find_matching_nodes with exact and partial matches."""
    paths: Paths = [["get", "status"], ["get", "config"], ["set", "value"]]
    tree = Tree(paths)

    # Exact match
    nodes = tree.find_matching_nodes("get status")
    assert len(nodes) == 1
    assert nodes[0].name == "status"
    assert nodes[0].parent.name == "get"

    # Partial match (deepest node)
    nodes = tree.find_matching_nodes("get stat")
    assert len(nodes) == 1
    assert nodes[0].name == "status"

    # Match intermediate node
    nodes = tree.find_matching_nodes("get")
    assert len(nodes) == 3
    assert "get" in [n.name for n in nodes]
    assert "status" in [n.name for n in nodes]
    assert "config" in [n.name for n in nodes]

    # No match
    nodes = tree.find_matching_nodes("post data")
    assert len(nodes) == 0

    # Match root
    nodes = tree.find_matching_nodes("")
    assert len(nodes) == 6
    assert "get" in [n.name for n in nodes]
    assert "set" in [n.name for n in nodes]
    assert "root" in [n.name for n in nodes]
    assert "status" in [n.name for n in nodes]
    assert "config" in [n.name for n in nodes]
    assert "value" in [n.name for n in nodes]

    # Test caching (call again, check cache)
    assert "get status" in tree.cache
    assert "get stat" in tree.cache
    assert "get" in tree.cache
    assert "" in tree.cache
    nodes_cached = tree.find_matching_nodes("get status")
    assert len(nodes_cached) == 1


def test_tree_find_matching_nodes_with_placeholders():
    """Tests find_matching_nodes with paths containing placeholders."""
    paths: Paths = [["set", "value ?"], ["set", "config ?"], ["get", "item ?"]]
    tree = Tree(paths)

    # Match placeholder path
    nodes = tree.find_matching_nodes("set value 123")
    assert len(nodes) == 1
    assert nodes[0].name == "value ?"

    # Partial match of placeholder value
    nodes = tree.find_matching_nodes("set value abc")
    assert len(nodes) == 1
    assert nodes[0].name == "value ?"

    # Match intermediate node before placeholder
    nodes = tree.find_matching_nodes("set")
    assert len(nodes) == 3  # Only the 'set' node itself
    assert "set" in [n.name for n in nodes]
    assert "value ?" in [n.name for n in nodes]
    assert "config ?" in [n.name for n in nodes]

    # Match multiple placeholder paths (should return deepest)
    nodes = tree.find_matching_nodes("set conf")
    assert len(nodes) == 1
    assert nodes[0].name == "config ?"

    # No match with placeholder structure
    nodes = tree.find_matching_nodes("set value")
    assert len(nodes) == 1
    assert nodes[0].name == "value ?"


def test_tree_get_suggestions():
    """Tests the get_suggestions method."""
    paths: Paths = [
        ["show", "config", "running"],
        ["show", "config", "startup"],
        ["show", "interfaces"],
        ["set", "value ?"],
    ]
    tree = Tree(paths)

    # Suggestions from root
    suggestions = tree.get_suggestions("")
    assert len(suggestions) == 8

    # Suggestions after partial command
    suggestions = tree.get_suggestions("sh")  # Partial
    expected = [
        "show",
        "show config",
        "show config running",
        "show config startup",
        "show interfaces",
    ]
    assert sorted(suggestions) == sorted(expected)

    # Suggestions after full command segment
    suggestions = tree.get_suggestions("show")
    assert sorted(suggestions) == sorted(expected)

    # Suggestions deeper in the tree
    suggestions = tree.get_suggestions("show config")
    assert sorted(suggestions) == sorted(
        ["show config", "show config running", "show config startup"]
    )

    # Suggestions with partial last segment
    suggestions = tree.get_suggestions("show config run")
    assert suggestions == ["show config running"]

    # Suggestions with placeholder
    suggestions = tree.get_suggestions("set val")
    assert suggestions == ["set value ?"]

    # Suggestions for exact match
    suggestions = tree.get_suggestions("show interfaces")
    assert suggestions == ["show interfaces"]

    # No suggestions for non-matching input
    suggestions = tree.get_suggestions("configure")
    assert suggestions == []

    # No suggestions when input is longer than any path
    suggestions = tree.get_suggestions("show interfaces brief")
    assert suggestions == []


def test_tree_suggestions_with_options_with_placeholders():
    "Testing suggestions past the fitst opion parameter with placeholder"
    paths: Paths = [
        ["show", "one ?"],
        ["show", "one ?", "two ?"],
        ["show", "config", "startup"],
    ]
    tree = Tree(paths)
    suggestions = tree.get_suggestions("show one")
    assert sorted(suggestions) == [
        "show one ?",
        "show one ? two ?"
    ]
    suggestions = tree.get_suggestions("show one domain")
    assert sorted(suggestions) == [
        "show one ?",
        "show one ? two ?"
    ]

    suggestions = tree.get_suggestions("show one domain t")
    assert sorted(suggestions) == [
        "show one ? two ?"
    ]




def test_tree_get_predictions():
    """Tests the get_suggestions method."""
    paths: Paths = [
        ["show", "config", "running"],
        ["show", "config", "startup"],
        ["show", "interfaces"],
        ["set", "value ?"],
    ]
    tree = Tree(paths)

    # Predictions from root
    predictions = tree.get_predictions("")
    assert sorted(predictions) == [
        "set", "show"
    ]

    # Predictions after partial command
    predictions = tree.get_predictions("sh")  # Partial
    assert predictions == ["show"]

    # Predictions after full command segment
    predictions = tree.get_predictions("show")
    assert predictions == ["show"]

    # Predictions after full command segment + space
    predictions = tree.get_predictions("show ")
    assert sorted(predictions) == [
        "show config",
        "show interfaces",
    ]

    # Predictions deeper in the tree
    predictions = tree.get_predictions("show config")
    assert predictions == ["show config"]

    # Predictions with partial last segment
    predictions = tree.get_predictions("show config run")
    assert predictions == ["show config running"]

    # Predictions with placeholder
    predictions = tree.get_predictions("set val")
    assert predictions == ["set value ?"]

    # Predictions with placeholder and value
    predictions = tree.get_predictions("set value 123")
    assert predictions == ["set value ?"]

    # Predictions for exact match
    predictions = tree.get_predictions("show interfaces")
    assert predictions == ["show interfaces"]

    # No predictions for non-matching input
    predictions = tree.get_predictions("configure")
    assert predictions == []

    # No predictions when input is longer than any path
    predictions = tree.get_predictions("show interfaces brief")
    assert predictions == []


def test_tree_get_prediction_with_options_with_placeholders():
    "Testing predictions past the fitst opion parameter with placeholder"
    paths: Paths = [
        ["show", "one ?"],
        ["show", "one ?", "two ?"],
        ["show", "config", "startup"],
    ]
    tree = Tree(paths)

    # before the first token
    predictions = tree.get_predictions("sh")  # Partial
    assert predictions == ["show"]

    # between first and second token
    predictions = tree.get_predictions("show ")
    assert sorted(predictions) == [
        "show config",
        "show one ?"
    ]

    # in the second token
    predictions = tree.get_predictions("show on")
    assert predictions == ["show one ?"]
    predictions = tree.get_predictions("show one domain")
    assert predictions == ["show one ?"]

    # after the second token
    predictions = tree.get_predictions("show one domain t")
    assert predictions == ["show one ? two ?"]
    predictions = tree.get_predictions("show one domain two access")
    assert predictions == ["show one ? two ?"]
