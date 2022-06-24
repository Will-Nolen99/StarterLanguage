import pytest
from interpreter.tokenizer import Tokenizer


def test_tokenizer_empty():
    test_file = "tests/tokenizer_test_files/empty_test.txt"

    tk = Tokenizer(test_file)
    tk.tokenize()

    target_token_stream = [50]
    target_literal_stream = ["EOF"]

    assert tk.token_stream == target_token_stream
    assert tk.token_literals == target_literal_stream


def test_tokenizer_single():
    test_file = "tests/tokenizer_test_files/single_token.txt"

    tk = Tokenizer(test_file)
    tk.tokenize()

    target_token_stream = [21, 50]
    target_literal_stream = ["%", "EOF"]

    assert tk.token_stream == target_token_stream
    assert tk.token_literals == target_literal_stream


def test_tokenizer_all():
    test_file = "tests/tokenizer_test_files/many_tokens.txt"

    tk = Tokenizer(test_file)
    tk.tokenize()

    target_token_stream = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        51,
        52,
        53,
        54,
        50,
    ]
    target_literal_stream = [
        "*=",
        "+=",
        "-=",
        "\=",
        "~=",
        "%=",
        "^=",
        ":=",
        "||",
        "&&",
        "++",
        "--",
        ">=",
        "<=",
        "==",
        "=",
        "+",
        "-",
        "*",
        "/",
        "%",
        "~",
        "!",
        "^",
        ":",
        "|",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "define",
        "int",
        "float",
        "boolean",
        "string",
        "array",
        "if",
        "else",
        "while",
        "do",
        "for",
        "true",
        "false",
        "12317432",
        "Hello World",
        "3.1415",
        "My_Var123",
        "EOF",
    ]

    assert tk.token_stream == target_token_stream
    assert tk.token_literals == target_literal_stream


def test_tokenizer_greedy_all():
    test_file = "tests/tokenizer_test_files/greedy_all_tokens.txt"

    tk = Tokenizer(test_file)
    tk.tokenize()

    target_token_stream = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        51,
        52,
        53,
        54,
        50,
    ]
    target_literal_stream = [
        "*=",
        "+=",
        "-=",
        "\=",
        "~=",
        "%=",
        "^=",
        ":=",
        "||",
        "&&",
        "++",
        "--",
        ">=",
        "<=",
        "==",
        "=",
        "+",
        "-",
        "*",
        "/",
        "%",
        "~",
        "!",
        "^",
        ":",
        "|",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "define",
        "int",
        "float",
        "boolean",
        "string",
        "array",
        "if",
        "else",
        "while",
        "do",
        "for",
        "true",
        "false",
        "12317432",
        "Hello World",
        "3.1415",
        "My_Var123",
        "EOF",
    ]

    assert tk.token_stream == target_token_stream
    assert tk.token_literals == target_literal_stream


def test_tokenizer_comment_single_line():
    test_file = "tests/tokenizer_test_files/single_line_comment.txt"

    tk = Tokenizer(test_file)
    tk.tokenize()

    target_token_stream = [52, 54, 17, 54, 15, 51, 52, 50]
    target_literal_stream = [
        "Hello  World",
        "X1",
        "+",
        "X2",
        "==",
        "14",
        "World",
        "EOF",
    ]

    assert tk.token_stream == target_token_stream
    assert tk.token_literals == target_literal_stream


def test_tokenizer_multi_line_comment_single_line():
    test_file = "tests/tokenizer_test_files/multi_line_comment_single_line.txt"

    tk = Tokenizer(test_file)
    tk.tokenize()

    target_token_stream = [52, 54, 52, 50]
    target_literal_stream = [
        "Hello  World",
        "X1",
        "World",
        "EOF",
    ]

    assert tk.token_stream == target_token_stream
    assert tk.token_literals == target_literal_stream


def test_tokenizer_multi_line_comment_multi_line():
    test_file = "tests/tokenizer_test_files/multi_line_comment.txt"

    tk = Tokenizer(test_file)
    tk.tokenize()

    target_token_stream = [52, 52, 50]
    target_literal_stream = [
        "Hello  World",
        "World",
        "EOF",
    ]

    assert tk.token_stream == target_token_stream
    assert tk.token_literals == target_literal_stream
