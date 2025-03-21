from pyrl_complete.parser import clear, paths, rules
import ply.lex as lex
import ply.yacc as yacc
import pytest


@pytest.fixture()
def parser():
    # setup
    lex.lex(module=rules)
    parser = yacc.yacc(module=rules)
    yield parser
    # teardown
    clear()


def test_one_tolken_only(parser: yacc):
    # put a semicolumn because it is a singlew line and there is
    # nocarriage return
    parser.parse("get;")
    assert len(paths()) == 1
    assert paths()[0] == ["get"]


def test_two_tokens_one_path(parser: yacc):
    parser.parse("get test;")
    assert len(paths()) == 1  # only one path
    assert paths()[0] == ["get", "test"]


def test_two_tokens_two_paths(parser: yacc):
    parser.parse("get | test;")
    assert len(paths()) == 2  # two paths
    assert paths()[0] == ["get"]
    assert paths()[1] == ["test"]


def test_two_tokens_two_paths_one_group(parser: yacc):
    parser.parse("(get | test);")
    assert len(paths()) == 2  # two paths
    assert paths()[0] == ["get"]
    assert paths()[1] == ["test"]


def test_two_tokens_three_paths_one_optional_group(parser: yacc):
    parser.parse("[get | test];")
    assert len(paths()) == 3
    assert paths()[0] == ["get"]
    assert paths()[1] == ["test"]
    assert paths()[2] == []


def test_three_tokens_two_paths_one_group(parser: yacc):
    parser.parse("one (get | test);")
    assert len(paths()) == 2
    assert paths()[0] == ["one", "get"]
    assert paths()[1] == ["one", "test"]
    # now change the order
    clear()
    parser.parse("(get | test) one;")
    assert len(paths()) == 2
    assert paths()[0] == ["get", "one"]
    assert paths()[1] == ["test", "one"]
    # assert ["test", "one"] in paths()


def test_three_tokens_three_paths_one_optional_group(parser: yacc):
    parser.parse("one [get | test];")
    assert len(paths()) == 3
    assert paths()[0] == ["one", "get"]
    assert paths()[1] == ["one", "test"]
    assert paths()[2] == ["one"]
    # now change the order
    clear()
    parser.parse("[get | test] one;")
    assert len(paths()) == 3
    assert paths()[0] == ["get", "one"]
    assert paths()[1] == ["test", "one"]
    assert paths()[2] == ["one"]


def test_two_groups(parser: yacc):
    parser.parse("(one | two | three) [get | test];")
    assert len(paths()) == 9
    assert paths()[0] == ["one", "get"]
    assert paths()[1] == ["one", "test"]
    assert paths()[2] == ["one"]
    assert paths()[3] == ["two", "get"]
    assert paths()[4] == ["two", "test"]
    assert paths()[5] == ["two"]
    assert paths()[6] == ["three", "get"]
    assert paths()[7] == ["three", "test"]
    assert paths()[8] == ["three"]
    # now change the order
    clear()
    parser.parse("[get | test] (one | two | three);")
    assert len(paths()) == 9
    assert paths()[0] == ["get", "one"]
    assert paths()[1] == ["get", "two"]
    assert paths()[2] == ["get", "three"]
    assert paths()[3] == ["test", "one"]
    assert paths()[4] == ["test", "two"]
    assert paths()[5] == ["test", "three"]
    assert paths()[6] == ["one"]
    assert paths()[7] == ["two"]
    assert paths()[8] == ["three"]


def test_option_with_arg(parser: yacc):
    parser.parse("get -d ? -a ?;")
    assert len(paths()) == 1
    assert ["get", "-d ?", "-a ?"] in paths()
    # now without spaces between option letter and ?
    clear()
    parser.parse("get -d? -a?;")
    assert len(paths()) == 1
    assert ["get", "-d ?", "-a ?"] in paths()
    # now with redundant ?
    clear()
    parser.parse("get -d ?? -a ??;")
    assert len(paths()) == 1
    assert ["get", "-d ?", "-a ?"] in paths()


def test_options_with_and_without_arg(parser: yacc):
    parser.parse("get -h | (-d ? -a ?);")
    assert len(paths()) == 2
    assert ["get", "-d ?", "-a ?"] in paths()
    assert ["get", "-h"] in paths()


def test_multi_lines(parser: yacc):
    data = """test | zero
            get zero (one | (two | three) )
            set (one | two) | zero
            get -h | (-d ? -a ? )
            test [first | second]
        """
    parser.parse(data)
    assert len(paths()) == 13
