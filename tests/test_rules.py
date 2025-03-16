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