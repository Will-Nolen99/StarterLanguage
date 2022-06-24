from tokenize import Token
from tokenizer import Tokenizer

test_file = "interpreter/test.txt"


tk = Tokenizer(test_file)
tk.tokenize()
