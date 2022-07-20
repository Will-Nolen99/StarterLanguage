from tokenizer import Tokenizer
from abstract_syntax_tree import Program
import sys


def main():

    test_file = sys.argv[1]

    tk = Tokenizer(test_file)
    tk.tokenize()

    program = Program(tk)
    program.parse()
    # program.print(out_file)
    program.execute()


if __name__ == "__main__":
    main()
