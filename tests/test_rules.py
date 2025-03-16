from pyrl.parser import clear,paths, rules
import ply.lex as lex
import ply.yacc as yacc
import pytest

@pytest.fixture()
def parser():
    #setup
    lexer = lex.lex(module=rules)
    parser = yacc.yacc(module=rules)
    yield parser
    #teardown
    clear()


def test_one_tolken_only(parser: yacc):
    parser.parse("get;") #put a semicolumn because it is a singlew line and there is no carriage return
    assert len(paths()) == 1
    assert paths()[0] == ["get"]

def test_two_tokens_one_path(parser: yacc):
    parser.parse("get test;") #put a semicolumn because it is a singlew line and there is no carriage return
    assert len(paths()) == 1  #only one path
    assert paths()[0] == ["get", "test"]

def test_two_tokens_two_paths(parser: yacc):
    parser.parse("get | test;")
    assert len(paths()) == 2  #two paths
    assert paths()[0] == ["get"]
    assert paths()[1] == ["test"]

def test_two_tokens_two_paths_one_group(parser: yacc):
    parser.parse("(get | test);")
    assert len(paths()) == 2  #two paths
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
    #now change the order
    clear()
    parser.parse("(get | test) one;")
    assert len(paths()) == 2
    assert paths()[0] == ["get","one"]
    assert paths()[1] == ["test","one"]

def test_three_tokens_three_paths_one_optional_group(parser: yacc):
    parser.parse("one [get | test];")
    assert len(paths()) == 3
    assert paths()[0] == ["one", "get"]
    assert paths()[1] == ["one", "test"]
    assert paths()[2] == ["one"]
    #now change the order
    clear()
    parser.parse("[get | test] one;")
    assert len(paths()) == 3
    assert paths()[0] == ["get", "one"]
    assert paths()[1] == ["test", "one"]
    assert paths()[2] == ["one"]