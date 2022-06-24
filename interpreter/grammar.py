class Syntax:

    symbols = {
        "=": 0,
        "*=": 1,
        "+=": 2,
        "-=": 3,
        "\=": 4,
        "~=": 5,
        "%=": 6,
        "^=": 7,
        ":=": 8,
        "||": 9,
        "&&": 10,
        "++": 11,
        "--": 12,
        "+": 13,
        "-": 14,
        "*": 15,
        "/": 16,
        "%": 17,
        "~": 18,
        "!": 19,
        "^": 20,
        ":": 21,
        "|": 22,
        "(": 23,
        ")": 24,
        "[": 25,
        "]": 26,
        "{": 27,
        "}": 28,
        "#": 29,
        "$": 30,
        '"': 31,
        "'": 32,
    }
    key_words = {
        "define": 33,
        "int": 34,
        "float": 35,
        "boolean": 36,
        "string": 37,
        "array": 38,
        "if": 39,
        "else": 40,
        "while": 41,
        "do": 42,
        "for": 43,
        "EOF": 44,
    }
