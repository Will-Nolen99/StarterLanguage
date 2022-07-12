from tokenizer import Tokenizer
from abstract_syntax_tree import Program


test_file = "interpreter/test.txt"
out_file = "interpreter/test_output.txt"


tk = Tokenizer(test_file)
tk.tokenize()

program = Program(tk)
program.parse()
program.print(out_file)

print("Finished")
