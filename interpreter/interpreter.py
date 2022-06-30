from tokenizer import Tokenizer
from abstract_syntax_tree import Program


test_file = "interpreter/test.txt"


tk = Tokenizer(test_file)
tk.tokenize()
