from pyrl_complete.parser import Node


def test_simple_tree():
    paths = [["get", "one"], ["get", "two"], ["set"]]
    root = Node("root", None)
    Node.populate_tree(root, paths)
    assert len(root.children) == 2
    assert len(root.children["get"].children) == 2
    assert root.children["get"].parent.name == "root"
    assert root.children["get"].children["one"].parent.name == "get"
    assert len(root.children["set"].children) == 0
