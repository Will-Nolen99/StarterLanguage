from tokenize import Token
from tokenizer import Tokenizer

test_file = "interpreter/grammar.py"


tk = Tokenizer(test_file)
tk.tokenize()
