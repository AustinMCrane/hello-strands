from agent import _count_char, count_char


def test_count_basic():
    assert _count_char("hello world", "l") == 3


def test_count_no_match():
    assert _count_char("hello", "z") == 0


def test_count_empty_string():
    assert _count_char("", "a") == 0


def test_count_case_sensitive():
    assert _count_char("Hello World", "h") == 0
    assert _count_char("Hello World", "H") == 1


def test_count_repeated():
    assert _count_char("mississippi", "s") == 4


def test_tool_name():
    assert count_char.tool_name == "count_char"
