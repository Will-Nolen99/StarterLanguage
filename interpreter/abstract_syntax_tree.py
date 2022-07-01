from tokenize import Token
from tokenizer import Tokenizer


class Program:

    functions = {}
    indentation_level = 0

    def __init__(self, tk: Tokenizer):
        self.tk = tk

    def parse(self):

        while self.tk.get_token() != Tokenizer.EOF:
            function = Function(self.tk)
            function.parse()
            new_name = function.name

            if new_name in Program.functions:
                message = f"A Function with this name already exists. End of duplicate function found on line {self.tk.get_line_number()}"
                raise DuplicateFunctionException(message)

            Program.functions[new_name] = function

        print("Done Parsing")

    def print(self, output_file):
        out_file = open(output_file, "a")
        for function in Program.functions:
            function.print(out_file)

        out_file.close()

    def execute(self):
        pass

    @staticmethod
    def indent():
        Program.indentation_level += 1

    @staticmethod
    def undent():
        Program.indentation_level -= 1

    @staticmethod
    def make_indent(out_file):
        out_file.write("\t" * Program.indentation_level)


class Function:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.name = None
        self.function_declaration_sequence = None
        self.Statement_Sequence = None
        self.Type = None

    def parse(self):

        # read define from token stream
        tk = self.tk
        if tk.get_token() != Tokenizer.key_words("define"):
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'define' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        # read name of function from the token stream
        if tk.get_token() != Tokenizer.name_token:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected function name found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        self.name = tk.get_literal()
        tk.skip_token()

        # read = from token stream
        if tk.get_token() != Tokenizer.symbols("="):
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '=' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        # read function declaration sequence from token stream
        self.function_declaration_sequence = Function_Declaration_Sequence(tk)
        self.function_declaration_sequence.parse()

        # read -> from token stream
        if tk.get_token() != Tokenizer.symbols("->"):
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '->' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        # read { from token stream
        open_brace = "{"
        if tk.get_token() != Tokenizer.symbols("{"):
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{open_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        # assign Statement Seequence
        self.Statement_Sequence = Statement_Sequence(tk)
        self.Statement_Sequence.parse()

        # read } from token stream
        close_brace = "}"
        if tk.get_token() != Tokenizer.symbols("{"):
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{close_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        # read -> from token stream
        if tk.get_token() != Tokenizer.symbols("->"):
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '->' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        # get return type for the function
        if (
            tk.get_token() < Tokenizer.key_words["int"]
            or tk.get_token() > Tokenizer.key_words["array"]
        ) and tk.get_token() != Tokenizer.key_words["nothing"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'data type' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        self.Type = tk.get_literal()
        tk.skip_token()

        # Parse function should be done now

    def print(self, out_file):
        out_file.write("define ")
        out_file.write(f"{self.name} ")
        out_file.write("= ")
        self.function_declaration_sequence.print(out_file)
        out_file.write(" -> {")
        Program.indend()
        self.Statement_Sequence.print(out_file)
        Program.undent()
        out_file.write("} -> ")
        out_file.write(f"{self.Type}")

    def execute(self):
        pass


class Function_Declaration_Sequence:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.function_declaration = None
        self.function_declaration_sequence = None
        self.alternative = None

    def parse(self):
        tk = self.tk

        self.function_declaration = Function_Declaration(tk)
        self.function_declaration.parse()

        token = tk.get_token()
        if token == Tokenizer.symbols[","]:
            self.alternative = 1
            tk.skip_token()

            self.function_declaration_sequence = Function_Declaration_Sequence(tk)
            self.function_declaration_sequence.parse()

        else:
            self.alternative = 2

    def print(self, out_file):
        self.function_declaration.print(out_file)
        if self.alternative == 1:
            out_file.write(", ")
            self.function_declaration_sequence.print(out_file)


class Function_Declaration:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.name = None
        self.type = None

    def parse(self):
        tk = self.tk

        # get type for function arguments
        if (
            tk.get_token() <= Tokenizer.key_words["int"]
            or tk.get_token() >= Tokenizer.key_words["array"]
        ):
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'data type' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        self.type = tk.get_literal()
        tk.skip_token()

        if tk.get_token() != Tokenizer.name_token:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'name' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        self.name = tk.get_literal()
        tk.skip_token()

    def print(self, out_file):
        out_file.write(f"{self.type} {self.name}")


class Statement_Sequence:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.statement = None
        self.statement_sequence = None
        self.alternative = None

    def parse(self):
        tk = self.tk

        self.statement = Statement(tk)
        self.statement.parse()
        self.alternative = 1

        token = tk.get_token()

        if (
            (
                token >= Tokenizer.key_words["int"]
                and token <= Tokenizer.key_words["array"]
            )
            or (token == Tokenizer.symbols["++"])
            or (token == Tokenizer.symbols["--"])
            or (token == Tokenizer.symbols["!"])
            or (token == Tokenizer.name_token)
            or (token == Tokenizer.key_words["if"])
            or (token == Tokenizer.key_words["do"])
            or (token == Tokenizer.key_words["while"])
            or (token == Tokenizer.key_words["for"])
            or (token == Tokenizer.key_words["print"])
            or (token == Tokenizer.key_words["read"])
        ):
            self.alternative = 2
            self.statement_sequence = Statement_Sequence(tk)
            self.statement_sequence.parse()

    def print(self, out_file):
        self.statement.print(out_file)
        if self.alternative == 1:
            self.statement_sequence.print(out_file)


class Declaration_Sequence:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.declaration = None
        self.declaration_sequence = None
        self.alternative = None

    def parse(self):
        tk = self.tk

        self.declaration = Declaration(tk)
        self.declaration.parse()
        self.alternative = 2

        token = tk.get_token()

        if token == Tokenizer.symbols[","]:
            tk.skip_token()
            self.alternative = 1
            self.declaration_sequence = Declaration_Sequence(tk)
            self.declaration_sequence.parse()

    def print(self, out_file):
        self.declaration.print(out_file)
        if self.alternative == 1:
            self.declaration_sequence.print(out_file)


class Statement:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.declaration_sequence = None
        self.expresssion = None
        self.if_statement = None
        self.while_statement = None
        self.do_while_statement = None
        self.for_statement = None
        self.input = None
        self.output = None

    def parse(self):
        tk = self.tk
        token = tk.get_token()

        if token == Tokenizer.key_words["if"]:
            self.alternative = 3
            self.if_statement = If(tk)
            self.if_statement.parse()

        elif token == Tokenizer.key_words["while"]:
            self.alternative = 4
            self.while_statement = While(tk)
            self.while_statement.parse()

        elif token == Tokenizer.key_words["do"]:
            self.alternative = 5
            self.do_while_statement = Do_While(tk)
            self.do_while_statement.parse()

        elif token == Tokenizer.key_words["for"]:
            self.alternative = 6
            self.for_statement = For(tk)
            self.for_statement.parse()

        elif token == Tokenizer.key_words["read"]:
            self.alternative = 7
            self.input = Input(tk)
            self.input.parse()

        elif token == Tokenizer.key_words["print"]:
            self.alternative = 8
            self.output = Output(tk)
            self.output.parse()

        elif (
            token >= Tokenizer.key_words["int"]
            and token <= Tokenizer.key_words["array"]
        ):
            self.alternative = 1
            self.declaration_sequence = Declaration_Sequence(tk)
            self.declaration_sequence.parse()

        else:
            self.alternative = 2
            self.expresssion = Expression(tk)
            self.expresssion.parse()

    def print(self, out_file):

        Program.make_indent()
        match self.alternative:
            case 1:
                self.declaration_sequence.print(out_file)
            case 2:
                self.expresssion.print(out_file)
            case 3:
                self.if_statement.print(out_file)
            case 3:
                self.while_statement.print(out_file)
            case 5:
                self.do_while_statement.print(out_file)
            case 6:
                self.for_statement.print(out_file)
            case 7:
                self.input.print(out_file)
            case 8:
                self.output.print(out_file)


class Declaration:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.type = None
        self.name = None
        self.or_statement = None

    def parse(self):
        tk = self.tk
        token = tk.get_token()

        if token < Tokenizer.key_words["int"] or token > Tokenizer.key_words["array"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'data type' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        self.type = tk.get_literal()
        tk.skip_token()

        token = tk.get_token()
        if token != Tokenizer.name_token:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'name' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        self.name = tk.get_literal()
        tk.skip_token()
        self.alternative = 1

        token = tk.get_token()
        if token == Tokenizer.symbols["="]:
            self.alternative = 2
            tk.skip_token()
            self.or_statement = Or(tk)
            self.or_statement.parse()

    def print(self, out_file):
        out_file.write(f"{self.type} {self.name}")
        if self.alternative == 2:
            out_file.write(" = ")
            self.or_statement.print(out_file)


class Expression:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.assignment = None
        self.or_expression = None

    def parse(self):

        tk = self.tokenizer
        token = tk.get_token()

        if token == Tokenizer.key_words["let"]:
            self.alternative = 2
            self.assignment = Assignment(tk)
            self.assignment.parse()

        else:
            self.alternative = 1
            self.or_expression = Or(tk)
            self.or_expression.parse()

    def print(self, out_file):
        if self.alternative == 1:
            self.or_expression.print(out_file)
        elif self.alternative == 2:
            self.assignment.print(out_file)


class If:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.expression = None
        self.statement_sequence = None
        self.statement_sequence2 = None
        self.if_statement = None

    def parse(self):

        tk = self.tk
        token = tk.get_token()

        self.alternative = 1
        if token != Tokenizer.key_words["if"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'if' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.expression = Expression(tk)
        self.expression.parse()

        open_brace = "{"
        token = tk.get_token()
        if token != Tokenizer.symbols["{"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{open_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.statement_sequence = Statement_Sequence(tk)
        self.statement_sequence.parse()

        close_brace = "}"
        token = tk.get_token()
        if token != Tokenizer.symbols["}"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{close_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        token = tk.get_token()
        if token != Tokenizer.key_words["else"]:
            return
        tk.skip_token()

        token = tk.get_token()
        if token == Tokenizer.symbols["{"]:
            self.alternative = 2
            tk.skip_token()
            self.statement_sequence2 = Statement_Sequence()
            self.statement_sequence2.parse()
        elif token == Tokenizer.key_words["if"]:
            self.alternative = 3
            self.if_statement = If(tk)
            self.if_statement.parse()

        else:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{open_brace}' or 'if' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)


class While:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.expression = None
        self.statement_sequence = None

    def parse(self):

        tk = self.tk

        self.expression = Expression(tk)
        self.expression.parse()

        token = tk.get_token()
        open_brace = "{"
        if token != Tokenizer.symbols["{"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{open_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.statement_sequence = Statement_Sequence(tk)
        self.statement_sequence.parse()

        token = tk.get_token()
        close_brace = "}"
        if token != Tokenizer.symbols["}"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{close_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()


class Do_While:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.expression = None
        self.statement_sequence = None

    def parse(self):
        tk = self.tk
        token = tk.get_token()

        if token != Tokenizer.key_words["do"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'do' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        token = tk.get_token()
        open_brace = "{"
        if token != Tokenizer.symbols["{"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{open_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.statement_sequence = Statement_Sequence(tk)
        self.statement_sequence.parse()

        token = tk.get_token()
        close_brace = "}"
        if token != Tokenizer.symbols["}"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{close_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        token = tk.get_token()
        if token != Tokenizer.key_words["while"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'while' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        self.expression = Expression(tk)
        self.expression.parse()


class For:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.declaration_sequence = None
        self.expression = None
        self.expression2 = None
        self.statement_sequence = None

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token != Tokenizer.key_words["for"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'for' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.declaration_sequence = Declaration_Sequence(tk)
        self.declaration_sequence.parse()

        token = tk.get_token()
        if token != Tokenizer.symbols["|"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '|' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.expression = Expression(tk)
        self.expression.parse()

        token = tk.get_token()
        if token != Tokenizer.symbols["|"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '|' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.expression2 = Expression(tk)
        self.expression2.parse()

        token = tk.get_token()
        open_brace = "{"
        if token != Tokenizer.symbols["{"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{open_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.statement_sequence = Statement_Sequence(tk)
        self.statement_sequence.parse()

        token = tk.get_token()
        close_brace = "}"
        if token != Tokenizer.symbols["}"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{close_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()


class Input:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.or_expression = None

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token != Tokenizer.key_words["input"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'input' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        token = tk.get_token()
        if token != Tokenizer.symbols["("]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '(' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.or_expression = Or(tk)
        self.or_expression.parse()

        token = tk.get_token()
        if token != Tokenizer.symbols[")"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected ')' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()


class Output:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.or_expression = None

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token != Tokenizer.key_words["print"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'print' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        token = tk.get_token()
        if token != Tokenizer.symbols["("]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '(' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.or_expression = Or(tk)
        self.or_expression.parse()

        token = tk.get_token()
        if token != Tokenizer.symbols[")"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected ')' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()


class Or:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.and_expression = None
        self.or_expression = None
        self.alternative = None

    def parse(self):
        tk = self.tk

        self.and_expression = And(tk)
        self.and_expression.parse()
        self.alternative = 1

        token = tk.get_token()
        if token == Tokenizer.symbols["||"]:
            tk.skip_token()
            self.alternative = 2
            self.or_expression = Or(tk)
            self.or_expression.parse()


class And:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.equality = None
        self.and_expression = None
        self.alternative = None

    def parse(self):
        tk = self.tk

        self.equality = Equality(tk)
        self.equality.parse()
        self.alternative = 1

        token = tk.get_token()
        if token == Tokenizer.symbols["&&"]:
            tk.skip_token()
            self.alternative = 2
            self.and_expression = And(tk)
            self.and_expression.parse()


class Equality:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.relational = None
        self.equality = None
        self.alternative = None

    def parse(self):
        tk = self.tk

        self.relational = Relational(tk)
        self.relational.parse()
        self.alternative = 1

        token = tk.get_token()

        if token == Tokenizer.symbols["=="]:
            tk.skip_token()
            self.alternative = 2
            self.equality = Equality(tk)
            self.equality.parse()
        elif token == Tokenizer.symbols["!="]:
            tk.skip_token()
            self.alternative = 3
            self.equality = Equality(tk)
            self.equality.parse()


class Relational:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.relational = None
        self.additive = None
        self.alternative = None

    def parse(self):
        tk = self.tk

        self.additive = Additive(tk)
        self.additive.parse()
        self.alternative = 1

        token = tk.get_token()
        if token == Tokenizer.symbols[">"]:
            tk.skip_token()
            self.relational = Relational(tk)
            self.alternative = 2
        elif token == Tokenizer.symbols[">="]:
            tk.skip_token()
            self.relational = Relational(tk)
            self.alternative = 3
        elif token == Tokenizer.symbols["<"]:
            tk.skip_token()
            self.relational = Relational(tk)
            self.alternative = 4
        elif token == Tokenizer.symbols["<="]:
            tk.skip_token()
            self.relational = Relational(tk)
            self.alternative = 5


class Additive:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.multiplicitive = None
        self.additive = None
        self.alternative = None

    def parse(self):
        tk = self.tk

        self.multiplicitive = Multiplicitive(tk)
        self.multiplicitive.parse()
        self.alternative = 1

        token = tk.get_token()
        if token == Tokenizer.symbols["+"]:
            self.alternative = 2
            self.additive = Additive(tk)
            self.additive.parse()

        elif token == Tokenizer.symbols["-"]:
            self.alternative = 3
            self.additive = Additive(tk)
            self.additive.parse()


class Multiplicitive:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.multiplicitive = None
        self.exponential = None

    def parse(self):
        tk = self.tk

        self.exponential = Exponential(tk)
        self.exponential.parse()
        self.alternative = 1

        token = tk.get_token()
        if token == Tokenizer.symbols["*"]:
            self.alternative = 2
            tk.skip_token()
            self.multiplicitive = Multiplicitive(tk)
            self.multiplicitive.parse()
        elif token == Tokenizer.symbols["/"]:
            self.alternative = 2
            tk.skip_token()
            self.multiplicitive = Multiplicitive(tk)
            self.multiplicitive.parse()
        elif token == Tokenizer.symbols["%"]:
            self.alternative = 2
            tk.skip_token()
            self.multiplicitive = Multiplicitive(tk)
            self.multiplicitive.parse()
        elif token == Tokenizer.symbols["~"]:
            self.alternative = 2
            tk.skip_token()
            self.multiplicitive = Multiplicitive(tk)
            self.multiplicitive.parse()


class Exponential:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.exponential = None
        self.unary = None

    def parse(self):
        tk = self.tk

        self.unary = Unary(tk)
        self.unary.parse()
        self.alternative = 1

        token = tk.get_token()
        if token == Tokenizer.symbols["^"]:
            self.alternative = 2
            tk.skip_token()
            self.exponential = Exponential(tk)
            self.exponential.parse()
        elif token == Tokenizer.symbols[":"]:
            self.alternative = 3
            tk.skip_token()
            self.exponential = Exponential(tk)
            self.exponential.parse()


class Unary:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.postfix = None
        self.unary = None

    def parse(self):
        tk = self.tk
        token = tk.get_token()

        if token == Tokenizer.symbols["++"]:
            self.alternative = 2
            tk.skip_token()
            self.unary = Unary(tk)
            self.unary.parse()
        elif token == Tokenizer.symbols["--"]:
            self.alternative = 3
            tk.skip_token()
            self.unary = Unary(tk)
            self.unary.parse()
        elif token == Tokenizer.symbols["!"]:
            self.alternative = 3
            tk.skip_token()
            self.unary = Unary(tk)
            self.unary.parse()
        else:
            self.alternative = 1
            self.postfix = Postfix(tk)
            self.postfix.parse()


class Postfix:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.term = None

    def parse(self):
        tk = self.tk

        self.term = Term(tk)
        self.term.parse()

        token = tk.get_token()
        if token == Tokenizer.symbols["++"]:
            self.alternative = 2
            tk.skip_token()

        elif token == Tokenizer.symbols["--"]:
            self.alternative = 3
            tk.skip_token()


class Term:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.or_statement = None
        self.var = None
        self.literal = None
        self.alternative = None

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token == Tokenizer.symbols["("]:
            tk.skip_token()
            self.alternative = 2
            self.or_statement = Or(tk)
            self.or_statement.parse()

            token = tk.get_token()
            if token != Tokenizer.symbols[")"]:
                message = f"Incorrect token found on line {tk.get_line_number()}. Expected '(' found '{tk.get_literal()}'."
                raise IncorrectTokenException(message)
            tk.skip_token()

        elif token == Tokenizer.name_token:
            self.alternative = 3
            self.var = Var(tk)
            self.var.parse()

        else:
            self.alternative = 1
            self.literal = Literal(tk)
            self.literal.parse()


class Literal:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.type = None
        self.value = None

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token == Tokenizer.integer_token:
            self.type = "int"
            self.value = int(tk.get_literal())
        elif token == Tokenizer.floating_point_token:
            self.type = "float"
            self.value = float(tk.get_literal())
        elif token == Tokenizer.string_token:
            self.type = "string"
            self.value = tk.get_literal()
        elif (
            token == Tokenizer.key_words["true"]
            or token == Tokenizer.key_words["false"]
        ):
            self.type = "boolean"
            self.value = token == Tokenizer.key_words["true"]

        elif token == ["["]:
            self.type = "array"
            array = ArrayLiteral(tk)
            array.parse()
            self.value = array.value
        else:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'literal' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)


class ArrayLiteral:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.value = []

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token != Tokenizer.symbols["["]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '(' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        token = tk.get_token()
        while token != Tokenizer.symbols["]"]:
            if token == Tokenizer.ssymbols[","]:
                tk.skip_token()
                token = tk.get_token()
                continue

            if (
                token != Tokenizer.integer_token
                and token != Tokenizer.floating_point_token
                and token != Tokenizer.string_token
                and token != Tokenizer.key_words["false"]
                and token != Tokenizer.key_words["true"]
            ):
                message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'value' found '{tk.get_literal()}'."
                raise IncorrectTokenException(message)

            if token == Tokenizer.key_words["false"]:
                self.value.append(False)
            elif token == Tokenizer.key_words["true"]:
                self.value.append(True)
            else:
                self.value.append(tk.get_literal())

            tk.skip_token()
            token = tk.get_token
        tk.skip_token()


class Var:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.array_access = None
        self.function_call = None
        self.name = None
        self.alternative = None

    def parse(self):
        tk = self.tk
        token = tk.get_token()

        if token != Tokenizer.name_token():
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'name' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        self.name = tk.get_literal()
        self.alternative = 4
        tk.skip_token()

        token = tk.get_token()
        if token == Tokenizer.symbols["("]:
            self.function_call = Function_Call(tk, self.name)
            self.function_call.parse()
            self.alternative = 3
        elif token == Tokenizer.symbols["["]:
            self.array_access = Array_Access(tk, self.name)
            self.array_access.parse()
            self.alternative = 2


class Function_Call:
    def __init__(self, tk: Tokenizer, name: str):
        self.tk = tk
        self.name = name
        self.expressions = []

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token != Tokenizer.symbols["("]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '(' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        token = tk.get_token()
        while token != Tokenizer.symbols[")"]:
            if token == Tokenizer.symbols[","]:
                tk.skip_token()
                token = tk.get_token()
                continue

            or_expresssion = Or(tk)
            or_expresssion.parse()
            self.expressions.append(or_expresssion)

            token = tk.get_token()


class Array_Access:
    def __init__(self, tk: Tokenizer, name: str):
        self.tk = tk
        self.name = name
        self.or_expression = None

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token != Tokenizer.symbols["["]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '[' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.or_expression = Or(tk)
        self.or_expression.parse()

        token = tk.get_token()
        if token != Tokenizer.symbols["]"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected ']' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()


class Assignment:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.left = None
        self.operator = None
        self.or_expression = None

    def parse(self):
        tk = self.tk

        self.left = Left()
        self.left.parse()

        token = tk.get_token()
        if token < Tokenizer.symbols["*="] or token > Tokenizer.symbols[":="]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'assignment operator' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        self.operator = tk.get_literal()

        self.or_expression = Or(tk)
        self.or_expression.parse()


class Left:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.name = None
        self.array_access = None
        self.alternative = None

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token != Tokenizer.name_token:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'name' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        self.name = tk.get_literal()
        tk.skip_token()
        self.alternative = 3

        token = tk.get_token()
        if token == Tokenizer.symbols["["]:
            self.alternative = 2
            self.array_access = Array_Access(tk, self.name)


class DuplicateFunctionException(Exception):
    def __init__(self, message):
        super().__init__(message)


class IncorrectTokenException(Exception):
    def __init__(self, message):
        super().__init__(message)
