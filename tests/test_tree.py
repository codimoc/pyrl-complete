from pyrl_complete.parser import Node


def test_simple_tree():
    paths = [["get", "one"], ["get", "two"], ["set"]]
    root = Node("root")
    Node.populate_tree(root, paths)
    assert len(root.children) == 2
    assert len(root.children["get"].children) == 2
    assert len(root.children["set"].children) == 0
    
