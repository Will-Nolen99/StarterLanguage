"""Class used to tokenize and input file into a stream of tokens to be used by the parser
"""


import re


class Tokenizer:

    symbols = {
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
        ">=": 13,
        "<=": 14,
        "==": 15,
        "=": 16,
        "+": 17,
        "-": 18,
        "*": 19,
        "/": 20,
        "%": 21,
        "~": 22,
        "!": 23,
        "^": 24,
        ":": 25,
        "|": 26,
        "(": 27,
        ")": 28,
        "[": 29,
        "]": 30,
        "{": 31,
        "}": 32,
        "#": 33,
        "$": 34,
        '"': 35,
        "'": 36,
    }

    key_words = {
        "define": 37,
        "int": 38,
        "float": 39,
        "boolean": 40,
        "string": 41,
        "array": 42,
        "if": 43,
        "else": 44,
        "while": 45,
        "do": 46,
        "for": 47,
        "true": 48,
        "false": 49,
        "EOF": 50,
    }

    integer = r"^([-]?[1-9]\d*|0)$"
    integer_token = 51

    string = r"^(\".*\")$"
    string_token = 52

    # this will mathch ints as well but as long as we check ints first it wont matter
    floating_point = r"^[-]?([0-9]*[.])?[0-9]+$"
    floating_point_token = 53

    def __init__(self, fname: str):
        self.fname = fname
        self.token_stream = []
        self.token_literals = []

    def tokenize(self):

        with open(self.fname) as source:
            for line in source:
                self.process(line)

    def process(self, line: str) -> None:

        line = line.strip()
        line = line.split()
        while line:

            token = line.pop(0)
            if token in Tokenizer.symbols:
                self.token_literal.append(token)
                self.token_steam.append(Tokenizer.symbols[token])

            elif token in Tokenizer.key_words:
                self.token_literals.append(token)
                self.token_stream.append(Tokenizer.key_words[token])

            elif re.search(Tokenizer.integer, token):
                self.token_literals.append(token)
                self.token_stream.append(Tokenizer.integer_token)

            elif re.search(Tokenizer.floating_point, token):
                self.token_literals.append(token)
                self.token_stream.append(Tokenizer.floating_point_token)

            elif re.search(Tokenizer.string, token):
                self.token_literals.append(token)
                self.token_stream.append(Tokenizer.string_token)

            else:
                # at this poiint it may be multiple symbols that are touching each other.
                # solve with greedy tokenization
                self.greedy_tokenize(token)

    def greedy_tokenize(token: str):
        pass

    def get_token(self) -> int:
        return self.token_stream[0]

    def skip_token(self) -> None:
        self.token_stream.pop(0)
        self.token_literals.pop(0)

    def get_literal(self) -> str:
        return self.token_literals[0]
