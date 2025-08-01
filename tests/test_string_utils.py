import pytest
from pyrl_complete.common.string_utils import (
    find_all_char_positions,
    is_word_char,
    remove_first_word,
    fill_placeholders_with_words,
)


# --- Tests for is_word_char ---


@pytest.mark.parametrize(
    "char_to_test, expected",
    [
        ("a", True),
        ("Z", True),
        ("5", True),
        ("_", True),
        (" ", False),
        ("-", False),
        ("?", False),
        (".", False),
    ],
)
def test_is_word_char(char_to_test, expected):
    """Tests is_word_char with various character types."""
    assert is_word_char(char_to_test) is expected


# --- Tests for remove_first_word ---


def test_remove_first_word_basic():
    """Tests basic removal of a word from the start of the string."""
    assert remove_first_word("hello world", 0) == " world"


def test_remove_first_word_from_middle():
    """Tests removing a word starting from an index in the middle of the string."""
    assert remove_first_word("first second third", 6) == "first  third"


def test_remove_first_word_start_index_inside_word():
    """
    Tests starting the search from within a word.
    The implementation finds the first word character at or after the index
    and removes the rest of that word.
    """
    assert remove_first_word("hello world", 2) == "he world"


def test_remove_first_word_with_leading_non_word_chars():
    """Tests removal when the word is preceded by non-word characters."""
    assert remove_first_word("  hello world", 0) == "   world"
    # Start search at the first 'h'
    assert remove_first_word("  hello world", 2) == "   world"


def test_remove_first_word_no_word_found():
    """Tests behavior when no word is found at or after the given index."""
    assert remove_first_word("hello ...", 5) == "hello ..."
    assert remove_first_word("... --- ...", 0) == "... --- ..."
    assert remove_first_word("word", 4) == "word"


def test_remove_first_word_invalid_index():
    """Tests that an out-of-bounds index returns the original string."""
    text = "some text"
    assert remove_first_word(text, -1) == text
    assert remove_first_word(text, len(text)) == text
    assert remove_first_word(text, len(text) + 5) == text


def test_remove_first_word_empty_string():
    """Tests behavior with an empty input string."""
    assert remove_first_word("", 0) == ""


def test_remove_first_word_at_end():
    """Tests removing the very last word of the string."""
    assert remove_first_word("the end", 4) == "the "


def test_remove_first_word_complex_word():
    """Tests removing a word containing letters, numbers, and underscores."""
    assert remove_first_word("this is a_word_123 and more", 8) == "this is  and more"


def test_remove_first_word_only_one_word():
    """Tests removing the only word in the string."""
    assert remove_first_word("supercalifragilisticexpialidocious", 0) == ""
    assert remove_first_word("supercalifragilisticexpialidocious", 10) == "supercalif"


# --- Tests for find_all_char_positions ---


@pytest.mark.parametrize(
    "text, char_to_find, expected",
    [
        ("hello world", "o", [4, 7]),
        ("abracadabra", "a", [0, 3, 5, 7, 10]),
        ("mississippi", "s", [2, 3, 5, 6]),
        ("no matching char", "z", []),
        ("character at the end", "d", [19]),
        ("start", "s", [0]),
        ("", "a", []),
        ("aaaaa", "a", [0, 1, 2, 3, 4]),
        ("!@#$%", "@", [1]),
    ],
)
def test_find_all_char_positions(text, char_to_find, expected):
    """Tests find_all_char_positions with various inputs."""
    assert find_all_char_positions(text, char_to_find) == expected


# --- Tests for fill_placeholders_with_words ---


@pytest.mark.parametrize(
    "prediction, input_str, expected",
    [
        # Basic cases with one or more placeholders
        (
            "set value ? for user ?",
            "set value 123 for user admin",
            "set value 123 for user admin",
        ),
        ("get item ?", "get item abc_123", "get item abc_123"),
        # No placeholders in prediction
        ("hello world", "this input is ignored", "hello world"),
        # Empty strings
        ("", "", ""),
        ("?", "", "?"),  # Cannot fill from empty input, should remain
        ("", "some word", ""),  # No placeholders to fill
        # Placeholders at start or end
        ("? world", "hello world", "hello world"),
        ("hello ?", "hello world", "hello world"),
        # Not enough words in input to fill all placeholders
        ("a ? b ? c", "a word1 b", "a word1 b ? c"),
        ("? ? ?", "one two", "one two ?"),
        # Input has extra words; they are ignored because matching is positional
        ("get ?", "get value from table", "get value"),
        # A placeholder that cannot be filled because no word is found at its position
        ("command --option ?", "command --option", "command --option ?"),
        # Word in input is shorter than the word it replaces (not really, it replaces '?')
        ("replace ? placeholder", "replace a placeholder", "replace a placeholder"),
        # Word in input is longer, causing the string to grow
        (
            "replace ? placeholder",
            "replace very_long_word placeholder",
            "replace very_long_word placeholder",
        ),
        # Multiple placeholders, but input string ends before the last one
        ("first ? second ? third ?", "first one second", "first one second ? third ?"),
    ],
)
def test_fill_placeholders_with_words(prediction, input_str, expected):
    """Tests fill_placeholders_with_words with various scenarios."""
    assert fill_placeholders_with_words(prediction, input_str) == expected
