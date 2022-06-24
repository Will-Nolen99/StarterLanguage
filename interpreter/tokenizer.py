"""Class used to tokenize and input file into a stream of tokens to be used by the parser
"""


import re
from tokenize import Token

from torch import _sparse_log_softmax_backward_data


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
        #'"': 35,
        # "'": 36,
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
    }

    EOF = 50

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
        self.line_number = 0

    def tokenize(self):

        with open(self.fname) as source:
            for line in source:
                self.line_number += 1
                self.__process(line)

    @staticmethod
    def __split(line: str):
        tokens = []

        while line:
            quote = False
            for i in range(len(line)):
                if line[i] == " " and not quote:

                    tokens.append(line[:i])
                    line = line[i + 1 :]
                    break

                if line[i] == '"':
                    quote = not quote

            else:
                tokens.append(line)
                return tokens

    def __process(self, line: str) -> None:

        line = line.strip()
        line = Tokenizer.__split(line)
        print(line)

        while line:

            token = line.pop(0)
            if token in Tokenizer.symbols:
                self.token_literals.append(token)
                self.token_stream.append(Tokenizer.symbols[token])

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
                self.__greedy_tokenize(token)

            print(self.token_stream)

    def __greedy_tokenize(self, token: str):

        symbol_list = list(Tokenizer.symbols)
        int_regex = Tokenizer.integer[:-1]
        float_regex = Tokenizer.floating_point[:-1]
        string_regex = Tokenizer.string[:-1]

        # symbol_list = ["\\" + symbol for symbol in symbol_list if "*" in symbol]

        while token:

            # scan token candidate from left to see if it multiple combined tokens
            for token_candidate in symbol_list:
                length = len(token_candidate)
                candidate = "\A" + re.escape(token_candidate)
                # print(candidate)

                if re.search(candidate, token):
                    found = token[:length]
                    self.token_literals.append(found)
                    self.token_stream.append(Tokenizer.symbols[token_candidate])
                    token = token[length:]
                    print("FOUND")
                    break

            else:
                if re.search(int_regex, token):
                    match = re.search(int_regex, token)
                    self.token_literals.append(match[0])
                    self.token_stream.append(Tokenizer.integer_token)
                    token = token[len(match[0]) :]

                elif re.search(float_regex, token):
                    match = re.search(float_regex, token)
                    self.token_literals.append(match[0])
                    self.token_stream.append(Tokenizer.floating_point_token)
                    token = token[len(match[0]) :]

                elif re.search(string_regex, token):
                    match = re.search(string_regex, token)
                    self.token_literals.append(match[0])
                    self.token_stream.append(Tokenizer.string_token)
                    token = token[len(match[0]) :]
                else:
                    message = f"Unknown token found on line {self.line_number}. {token} is not recognized."
                    raise UnknownTokenException(message)

    def get_token(self) -> int:
        return self.token_stream[0]

    def skip_token(self) -> None:
        self.token_stream.pop(0)
        self.token_literals.pop(0)

    def get_literal(self) -> str:
        return self.token_literals[0]


class UnknownTokenException(Exception):
    def __init__(self, message):
        super().__init__(message)
