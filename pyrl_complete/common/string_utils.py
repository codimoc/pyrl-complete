from typing import List


def is_word_char(c: chr) -> bool:
    """Checks if a character is considered part of a 'word'.

    A word character is defined as any alphanumeric character (a-z, A-Z, 0-9)
    or an underscore (_).

    Args:
        c: The character to check.

    Returns:
        True if the character is a word character, False otherwise.
    """
    return c.isalnum() or c == "_"


def remove_first_word(text: str, index: int) -> str:
    """Removes the first word in a string at or after a given index.

    A "word" is a sequence of alphanumeric characters or underscores as
    defined by `is_word_char`.

    Args:
        text: The input string.
        index: The position to start searching for a word to remove.

    Returns:
        The string with the word removed, or the original string if no
        word is found or the index is invalid.
    """
    if index < 0 or index >= len(text):
        return text
    word_start = -1
    for i in range(index, len(text)):
        if is_word_char(text[i]):
            word_start = i
            break
    if word_start == -1:
        return text
    word_end = word_start
    while word_end < len(text) and is_word_char(text[word_end]):
        word_end += 1
    return text[:word_start] + text[word_end:]


def find_all_char_positions(text: str, char_to_find: chr) -> List[int]:
    """Finds all positions of a given character in a string.

    Args:
        text: The input string to search within.
        char_to_find: The character to find.

    Returns:
        A list of integer indices for all occurrences of the character.
        Returns an empty list if the character is not found.
    """
    return [i for i, char in enumerate(text) if char == char_to_find]
