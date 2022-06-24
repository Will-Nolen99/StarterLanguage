"""Class used to tokenize and input file into a stream of tokens to be used by the parser
"""


class Tokenizer:
    def __init__(self, fname: str):
        self.fname = fname
        self.token_stream = []
        self.token_literals = []

    def tokenize(self):

        with open(self.fname) as source:
            for line in source:
                pass

    def get_token(self) -> int:
        return self.token_stream[0]

    def skip_token(self) -> None:
        self.token_stream.pop(0)
        self.token_literals.pop(0)

    def get_literal(self) -> str:
        return self.token_literals[0]
