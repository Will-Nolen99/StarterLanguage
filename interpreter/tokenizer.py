"""Class used to tokenize and input file into a stream of tokens to be used by the parser
"""


import re
from tokenize import Token

from numpy import string_


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
        # "#": 33,
        # "$": 34,
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
    floating_point = r"^[-]?([0-9]*)?[.][0-9]+$"
    floating_point_token = 53

    name = r"^[\w]+$"
    name_token = 54

    def __init__(self, fname: str):
        self.fname = fname
        self.token_stream = []
        self.token_literals = []
        self.line_number = 0
        self.in_comment = False

    def tokenize(self):

        with open(self.fname) as source:
            for line in source:
                self.line_number += 1
                if line == "":
                    continue
                self.__process(line)

        self.token_stream.append(Tokenizer.EOF)
        self.token_literals.append("EOF")

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

        while line:

            token = line.pop(0)

            # check for comments
            if token == "#":
                return  # skip rest of line in single line comment

            if token == "$":
                self.in_comment = not self.in_comment
                continue

            if token in Tokenizer.symbols and not self.in_comment:

                self.token_literals.append(token)
                self.token_stream.append(Tokenizer.symbols[token])

            elif token in Tokenizer.key_words and not self.in_comment:
                self.token_literals.append(token)
                self.token_stream.append(Tokenizer.key_words[token])

            elif re.search(Tokenizer.integer, token) and not self.in_comment:
                self.token_literals.append(token)
                self.token_stream.append(Tokenizer.integer_token)

            elif re.search(Tokenizer.floating_point, token) and not self.in_comment:
                self.token_literals.append(token)
                self.token_stream.append(Tokenizer.floating_point_token)

            elif re.search(Tokenizer.string, token) and not self.in_comment:
                self.token_literals.append(token.strip('"'))
                self.token_stream.append(Tokenizer.string_token)

            elif re.search(Tokenizer.name, token) and not self.in_comment:
                self.token_literals.append(token)
                self.token_stream.append(Tokenizer.name_token)

            else:
                # at this poiint it may be multiple symbols that are touching each other.
                # solve with greedy tokenization
                comment = self.__greedy_tokenize(token)
                if comment:
                    return

    def __greedy_tokenize(self, token: str):

        symbol_list = list(Tokenizer.symbols)
        int_regex = Tokenizer.integer[:-1]
        float_regex = Tokenizer.floating_point[:-1]
        string_regex = Tokenizer.string[:-1]
        name_regex = Tokenizer.name[:-1]

        while token:

            if token[0] == "#" and not self.in_comment:
                return True

            if token[0] == "$":
                self.in_comment = not self.in_comment
                token = token[1:]
                continue

            # scan token candidate from left to see if it multiple combined tokens
            for token_candidate in symbol_list:
                length = len(token_candidate)
                candidate = "\A" + re.escape(token_candidate)

                if re.search(candidate, token):
                    found = token[:length]
                    if not self.in_comment:
                        self.token_literals.append(found)
                        self.token_stream.append(Tokenizer.symbols[token_candidate])
                    token = token[length:]
                    break

            else:
                if re.search(float_regex, token):
                    match = re.search(float_regex, token)
                    if not self.in_comment:
                        self.token_literals.append(match[0])
                        self.token_stream.append(Tokenizer.floating_point_token)
                    token = token[len(match[0]) :]

                elif re.search(int_regex, token):
                    match = re.search(int_regex, token)
                    if not self.in_comment:
                        self.token_literals.append(match[0])
                        self.token_stream.append(Tokenizer.integer_token)
                    token = token[len(match[0]) :]

                elif re.search(string_regex, token):
                    match = re.search(string_regex, token)
                    current_string = match[0].strip('"')
                    if not self.in_comment:
                        self.token_literals.append(current_string)
                        self.token_stream.append(Tokenizer.string_token)
                    token = token[len(match[0]) :]

                elif re.search(name_regex, token):
                    match = re.search(name_regex, token)
                    if not self.in_comment:
                        self.token_literals.append(match[0])
                        self.token_stream.append(Tokenizer.name_token)
                    token = token[len(match[0]) :]

                else:
                    if not self.in_comment:
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
