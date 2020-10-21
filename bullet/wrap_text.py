import re

WORD_REGEX = re.compile(r"\s?(?P<word>\b\w+\b)\s?")


def wrap_text(s: str, max_len: int):
    """Wrap text at word boundaries.
    Args:
        s (str): The string to be wrapped.
        max_len (int): Maximum length of each substring
    Returns:
        str: String that will display a multiline string where the length of
            each line is less than or equal to  max_len. Wrapping will not
            occur in the middle of a word for prettier output.
    """
    substrings = []
    while True:
        if len(s) <= max_len:
            substrings.append(s)
            break
        (wrapped, s) = _wrap_string(s, max_len)
        substrings.append(wrapped)
    return "\n".join(substrings)


def _wrap_string(s, max_len):
    last_word_boundary = max_len
    for match in WORD_REGEX.finditer(s):
        if match.end("word") > max_len:
            break
        last_word_boundary = match.end("word") + 1
    wrapped = s[:last_word_boundary]
    s = s[last_word_boundary:].strip()
    return (wrapped, s)
