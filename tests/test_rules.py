from pyrl_complete.parser import Parser
from pyrl_complete.parser.rules import merge
import pytest


@pytest.fixture()
def my_parser():
    # setup
    yield Parser()
    # teardown


def test_one_tolken_only(my_parser: Parser):
    # put a semicolumn because it is a singlew line and there is
    # nocarriage return
    my_parser.parse("get;")
    assert len(my_parser.paths) == 1
    assert my_parser.paths[0] == ["get"]


def test_two_tokens_one_path(my_parser: Parser):
    my_parser.parse("get test;")
    assert len(my_parser.paths) == 1  # only one path
    assert my_parser.paths[0] == ["get", "test"]


def test_two_tokens_two_paths(my_parser: Parser):
    my_parser.parse("get | test;")
    assert len(my_parser.paths) == 2  # two paths
    assert my_parser.paths[0] == ["get"]
    assert my_parser.paths[1] == ["test"]


def test_two_tokens_two_paths_one_group(my_parser: Parser):
    my_parser.parse("(get | test);")
    assert len(my_parser.paths) == 2  # two paths
    assert my_parser.paths[0] == ["get"]
    assert my_parser.paths[1] == ["test"]


def test_two_tokens_three_paths_one_optional_group(my_parser: Parser):
    my_parser.parse("[get | test];")
    assert len(my_parser.paths) == 3
    assert my_parser.paths[0] == ["get"]
    assert my_parser.paths[1] == ["test"]
    assert my_parser.paths[2] == []


def test_three_tokens_two_paths_one_group(my_parser: Parser):
    my_parser.parse("one (get | test);")
    assert len(my_parser.paths) == 2
    assert my_parser.paths[0] == ["one", "get"]
    assert my_parser.paths[1] == ["one", "test"]
    # now change the order
    my_parser.parse("(get | test) one;")
    assert len(my_parser.paths) == 2
    assert my_parser.paths[0] == ["get", "one"]
    assert my_parser.paths[1] == ["test", "one"]
    # assert ["test", "one"] in my_parser.paths


def test_three_tokens_three_paths_one_optional_group(my_parser: Parser):
    my_parser.parse("one [get | test];")
    assert len(my_parser.paths) == 3
    assert my_parser.paths[0] == ["one", "get"]
    assert my_parser.paths[1] == ["one", "test"]
    assert my_parser.paths[2] == ["one"]
    # now change the order
    my_parser.parse("[get | test] one;")
    assert len(my_parser.paths) == 3
    assert my_parser.paths[0] == ["get", "one"]
    assert my_parser.paths[1] == ["test", "one"]
    assert my_parser.paths[2] == ["one"]


def test_two_groups(my_parser: Parser):
    my_parser.parse("(one | two | three) [get | test];")
    assert len(my_parser.paths) == 9
    assert my_parser.paths[0] == ["one", "get"]
    assert my_parser.paths[1] == ["one", "test"]
    assert my_parser.paths[2] == ["one"]
    assert my_parser.paths[3] == ["two", "get"]
    assert my_parser.paths[4] == ["two", "test"]
    assert my_parser.paths[5] == ["two"]
    assert my_parser.paths[6] == ["three", "get"]
    assert my_parser.paths[7] == ["three", "test"]
    assert my_parser.paths[8] == ["three"]
    # now change the order
    my_parser.parse("[get | test] (one | two | three);")
    assert len(my_parser.paths) == 9
    assert my_parser.paths[0] == ["get", "one"]
    assert my_parser.paths[1] == ["get", "two"]
    assert my_parser.paths[2] == ["get", "three"]
    assert my_parser.paths[3] == ["test", "one"]
    assert my_parser.paths[4] == ["test", "two"]
    assert my_parser.paths[5] == ["test", "three"]
    assert my_parser.paths[6] == ["one"]
    assert my_parser.paths[7] == ["two"]
    assert my_parser.paths[8] == ["three"]


def test_option_with_arg(my_parser: Parser):
    my_parser.parse("get -d ? -a ?;")
    assert len(my_parser.paths) == 1
    assert ["get", "-d ?", "-a ?"] in my_parser.paths
    # now without spaces between option letter and ?
    my_parser.parse("get -d? -a?;")
    assert len(my_parser.paths) == 1
    assert ["get", "-d ?", "-a ?"] in my_parser.paths
    # now with redundant ?
    my_parser.parse("get -d ?? -a ??;")
    assert len(my_parser.paths) == 1
    assert ["get", "-d ?", "-a ?"] in my_parser.paths
    # now an option of lenght 2
    my_parser.parse("get -ik ? -iv ?;")
    assert len(my_parser.paths) == 1
    assert ["get", "-ik ?", "-iv ?"] in my_parser.paths


def test_three_letter_option_with_arg(my_parser: Parser):
    my_parser.parse("get -abc ? -def ?;")
    assert len(my_parser.paths) == 1
    assert ["get", "-abc ?", "-def ?"] in my_parser.paths


def test_options_with_and_without_arg(my_parser: Parser):
    my_parser.parse("get -h | (-d ? -a ?);")
    assert len(my_parser.paths) == 2
    assert ["get", "-d ?", "-a ?"] in my_parser.paths
    assert ["get", "-h"] in my_parser.paths


def test_multi_lines(my_parser: Parser):
    data = """test | zero
            get zero (one | (two | three) )
            set (one | two) | zero
            get -h | (-d ? -a ? )
            test [first | second]
        """
    my_parser.parse(data)
    assert len(my_parser.paths) == 13


def test_two_lines_with_statement_endings(my_parser: Parser):
    data = """test | zero;
            get zero (one | (two | three) );
        """
    my_parser.parse(data)
    assert len(my_parser.paths) == 5

# --- Tests for merge function ---


def test_merge_empty():
    assert merge([], []) == []
    assert merge([["a"]], []) == [["a"]]
    assert merge([], [["b"]]) == [["b"]]
    assert merge(None, [["b"]]) == [["b"]]
    assert merge([["a"]], None) == [["a"]]
    assert merge(None, None) is None  # Based on current implementation


def test_merge_simple():
    l1 = [["a"], ["b"]]
    l2 = [["1"], ["2"]]
    expected = [["a", "1"], ["a", "2"], ["b", "1"], ["b", "2"]]
    assert merge(l1, l2) == expected


def test_merge_complex():
    l1 = [["a", "b"], ["c"]]
    l2 = [["1", "2"]]
    expected = [["a", "b", "1", "2"], ["c", "1", "2"]]
    assert merge(l1, l2) == expected
