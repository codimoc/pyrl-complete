from pyrl_complete.parser import Parser, clear, paths
import pytest


@pytest.fixture()
def my_parser():
    # setup
    yield Parser()
    # teardown
    clear()  # Ensure paths are cleared after each test using this fixture


def test_clear(my_parser: Parser):
    my_parser.parse("get test;")
    assert len(paths()) == 1
    clear()
    assert len(paths()) == 0

