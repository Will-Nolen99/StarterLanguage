from ast import match_case

from numpy import var
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
        out_file = open(output_file, "w")
        for name, function in Program.functions.items():
            function.print(out_file)
            out_file.write("\n")

        out_file.close()

    def execute(self):
        if "main" in Program.functions:
            Program.functions.execute()
        else:
            print("No main function found.")

    @staticmethod
    def indent():
        Program.indentation_level += 1

    @staticmethod
    def undent():
        Program.indentation_level -= 1

    @staticmethod
    def make_indent(out_file):
        out_file.write("\t" * Program.indentation_level)

    @staticmethod
    def type_check(value, var_type) -> bool:

        match var_type:
            case "boolean":
                return value in ["true", "false", True, False]
            case "string":
                return isinstance(value, str)
            case "int":
                return isinstance(value, int)
            case "float":
                return isinstance(value, float)
            case "array":
                return isinstance(value, list)

    @staticmethod
    def attempt_convert(value, type):

        converted = None
        match type:
            case "boolean":
                converted = bool(value)
            case "string":
                converted = value
            case "int":
                converted = int(value)
            case "float":
                converted = float(value)
            case "array":
                # TODO make a better convention
                converted = list(value)

        return converted


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
        if tk.get_token() != Tokenizer.key_words["define"]:
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
        if tk.get_token() != Tokenizer.symbols["="]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '=' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        # read function declaration sequence from token stream
        self.function_declaration_sequence = Function_Declaration_Sequence(tk)
        self.function_declaration_sequence.parse()

        # read -> from token stream
        if tk.get_token() != Tokenizer.symbols["->"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '->' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        # read { from token stream
        open_brace = "{"
        if tk.get_token() != Tokenizer.symbols["{"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{open_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        # assign Statement Seequence
        self.Statement_Sequence = Statement_Sequence(tk)
        self.Statement_Sequence.parse()

        # read } from token stream
        close_brace = "}"
        if tk.get_token() != Tokenizer.symbols["}"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{close_brace}' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        # read -> from token stream
        if tk.get_token() != Tokenizer.symbols["->"]:
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
        out_file.write(" -> {\n")
        Program.indent()
        self.Statement_Sequence.print(out_file)
        Program.undent()
        out_file.write("} -> ")
        out_file.write(f"{self.Type}\n")

    def execute(self, values: list):
        var_names, var_types = self.function_declaration_sequence.execute()

        if len(values) != len(var_names):
            message = f"Function {self.name} takes {len(var_names)} arguments.  {len(values)} where given."
            raise ArgumentParameterMismatchException(message)

        function_types = dict(zip(var_types, values))
        function_vars = dict(zip(var_names, values))

        for name in var_names:
            if not Program.type_check(function_vars[name], function_types[name]):
                message = f"Incorrect type in function {self.name}. {name} should be {function_types[name]}"
                raise TypeMismatchException(message)

        self.Statement_Sequence.execute(function_vars, function_types)
        # may need to add things here I forgot what I was doing


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

    def execute(self):
        var_names = []
        var_types = []

        var_name, var_type = self.function_declaration.execute()
        var_names.append(var_name)
        var_types.append(var_type)

        if self.alternative == 1:
            (
                rest_var_names,
                rest_var_types,
            ) = self.function_declaration_sequence.execute()
            var_names += rest_var_names
            var_types += rest_var_types

        return var_names, var_types


class Function_Declaration:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.name = None
        self.type = None

    def parse(self):
        tk = self.tk

        # get type for function arguments
        if (
            tk.get_token() < Tokenizer.key_words["int"]
            or tk.get_token() > Tokenizer.key_words["array"]
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

    def execute(self):
        return self.name, self.type


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
            or (token == Tokenizer.key_words["return"])
            or (token == Tokenizer.key_words["let"])
        ):
            self.alternative = 2
            self.statement_sequence = Statement_Sequence(tk)
            self.statement_sequence.parse()

    def print(self, out_file):
        self.statement.print(out_file)
        if self.alternative == 2:
            self.statement_sequence.print(out_file)

    def execute(self, values, types):
        self.statement.execute(values, types)

        if self.alternative == 2:
            self.statement_sequence.execute(values, types)


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
            out_file.write(", ")
            self.declaration_sequence.print(out_file)

    def execute(self, values, types):
        self.declaration.execute(values, types)
        if self.alternative == 1:
            self.declaration_sequence.execute(values, types)


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
        self.ret = None

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

        elif token == Tokenizer.key_words["return"]:
            self.alternative = 9
            self.ret = Return(tk)
            self.ret.parse()

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

        Program.make_indent(out_file)
        match self.alternative:
            case 1:
                self.declaration_sequence.print(out_file)
            case 2:
                self.expresssion.print(out_file)
            case 3:
                self.if_statement.print(out_file)
            case 4:
                self.while_statement.print(out_file)
            case 5:
                self.do_while_statement.print(out_file)
            case 6:
                self.for_statement.print(out_file)
            case 7:
                self.input.print(out_file)
            case 8:
                self.output.print(out_file)
            case 9:
                self.ret.print(out_file)

        out_file.write("\n")

    def execute(self, values, types):
        match self.alternative:
            case 1:
                self.declaration_sequence.execute(values, types)
            case 2:
                self.expression.execute(values, types)
            case 3:
                self.if_statement.execute(values, types)
            case 4:
                self.while_statement.execute(values, types)
            case 5:
                self.do_while_statement.execute(values, types)
            case 6:
                self.for_statement.execute(values, types)
            case 7:
                self.input.execute(values, types)
            case 8:
                self.output.execute(values, types)
            case 9:
                self.ret.execute(values, types)


class Return:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.name = None
        self.expression = None

    def parse(self):
        tk = self.tk
        token = tk.get_token()

        if token != Tokenizer.key_words["return"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'return' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        tk.skip_token()
        token = tk.get_token()

        if token == Tokenizer.name_token:
            self.name = tk.get_literal()
            self.alternative = 1
            tk.skip_token()

        else:
            self.expression = Expression(tk)
            self.alternative = 2
            self.expression.parse()

    def print(self, out_file):
        out_file.write("return ")
        if self.alternative == 1:
            out_file.write(f"{self.name}")
        elif self.alternative == 2:
            self.expression.print(out_file)

    def execute(self, values, types):
        if self.alternative == 1:
            if self.name not in values:
                message = f"{self.name} has not been declared."
                raise UndeclaredVariableException(message)
            return values[self.name]
        elif self.alternative == 2:
            return self.expression.execute(values, types)


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

    def execute(self, values, types):
        if self.name in values:
            message = f"{self.name} has alraedy been declared."
            raise DuplicateVariableException(message)

        value = self.or_statement.execute(values, types)
        types[self.name] = self.type
        if Program.type_check(value, self.type):
            values[self.name] = value
        else:
            message = (
                f"{self.name}  is of type {self.type} but recieved a value of {value}."
            )
            raise TypeMismatchException(message)


class Expression:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.assignment = None
        self.or_expression = None

    def parse(self):

        tk = self.tk
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

    def execute(self, values, types):
        if self.alternative == 2:
            self.assignment.execute(values, types)
        elif self.alternative == 1:
            return self.or_expression.execute(values, types)


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
            self.statement_sequence2 = Statement_Sequence(tk)
            self.statement_sequence2.parse()

            token = tk.get_token()
            if token != Tokenizer.symbols["}"]:
                close_brace = "}"
                message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{close_brace}' or 'if' found '{tk.get_literal()}'."
                raise IncorrectTokenException(message)
            tk.skip_token()

        elif token == Tokenizer.key_words["if"]:
            self.alternative = 3
            self.if_statement = If(tk)
            self.if_statement.parse()

        else:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected '{open_brace}' or 'if' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

    def print(self, out_file):
        out_file.write("if ")
        self.expression.print(out_file)
        out_file.write(" {\n")
        Program.indent()

        self.statement_sequence.print(out_file)
        Program.undent()
        Program.make_indent(out_file)
        out_file.write("}")
        if self.alternative == 2 or self.alternative == 3:
            out_file.write(" else ")
            if self.alternative == 3:
                self.if_statement.print(out_file)
            else:
                Program.indent()
                out_file.write("{\n")
                self.statement_sequence2.print(out_file)
                Program.undent()
                Program.make_indent(out_file)
                out_file.write("}")

    def execute(self, values, types):
        condition = self.expression.execute(values, types)
        if condition:
            return self.statement_sequence.execute(values, types)
        elif self.alternative == 2:
            return self.statement_sequence2.execute(values, types)
        elif self.alternative == 3:
            return self.if_statement.execute(values, types)


class While:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.expression = None
        self.statement_sequence = None

    def parse(self):
        tk = self.tk
        token = tk.get_token()

        if token != Tokenizer.key_words["while"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'while' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        tk.skip_token()

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

    def print(self, out_file):
        out_file.write("while ")
        self.expression.print(out_file)
        out_file.write(" {\n")
        Program.indent()
        self.statement_sequence.print(out_file)
        Program.undent()
        Program.make_indent(out_file)
        out_file.write("}")

    def execute(self, values, types):
        while self.expression.execute(values, types):
            x = self.statement_sequence.execute(values, types)
            # using x here as temperary precaution incase of early terminations and returns


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
        tk.skip_token()

        self.expression = Expression(tk)
        self.expression.parse()

    def print(self, out_file):
        out_file.write("do {\n")
        Program.indent()
        self.statement_sequence.print(out_file)
        Program.undent()
        Program.make_indent(out_file)
        out_file.write("} while ")
        self.expression.print(out_file)

    def execute(self, values, types):
        y = self.statement_sequence.execute(values, types)
        while self.condition.execute(values, types):
            x = self.statement_sequence.execute(values, types)


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

    def print(self, out_file):
        out_file.write("for ")
        self.declaration_sequence.print(out_file)
        out_file.write(" | ")
        self.expression.print(out_file)
        out_file.write(" | ")
        self.expression2.print(out_file)
        out_file.write(" {\n")
        Program.indent()
        self.statement_sequence.print(out_file)
        Program.undent()
        Program.make_indent(out_file)
        out_file.write("}")

    def execute(self, values, types):
        self.declaration_sequence.execute(values, types)
        while self.expression.execute(values, types):
            x = self.statement_sequence.execute(values, types)
            self.expression2.execute(values, types)


class Input:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.or_expression = None
        self.name = None
        self.alternative = 1

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token != Tokenizer.key_words["read"]:
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
        if token == Tokenizer.symbols[","]:
            self.alternative = 2
            tk.skip_token()
            token = tk.get_token()
            if token != Tokenizer.name_token:
                message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'name' found '{tk.get_literal()}'."
                raise IncorrectTokenException(message)

            self.name = tk.get_literal()
            tk.skip_token()

        token = tk.get_token()
        if token != Tokenizer.symbols[")"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected ')' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

    def print(self, out_file):
        out_file.write("read(")
        self.or_expression.print(out_file)
        if self.alternative == 2:
            out_file.write(f", {self.name}")
        out_file.write(")")

    def execute(self, values, types):
        string = self.or_expression.execute(values, types)
        std_in = input(string)
        converted_std_in = Program.attempt_convert(std_in)
        values[self.name] = converted_std_in


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

    def print(self, out_file):
        out_file.write("print(")
        self.or_expression.print(out_file)
        out_file.write(")")

    def execute(self, values, types):
        string = self.or_expression.execute(values, types)
        print(string)


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

    def print(self, out_file):
        self.and_expression.print(out_file)
        if self.alternative == 2:
            out_file.write(" || ")
            self.or_expression.print(out_file)

    def execute(self, values, types):
        v1 = self.and_expression.execute(values, types)
        if self.alternative == 2:
            v2 = self.or_expression.execute(values, types)
            return v1 or v2
        return v1


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

    def print(self, out_file):
        self.equality.print(out_file)
        if self.alternative == 2:
            out_file.write(" && ")
            self.and_expression.print(out_file)

    def execute(self, values, types):
        v1 = self.equality.execute(values, types)
        if self.alternative == 2:
            v2 = self.and_expression.execute(values, types)
            return v1 and v2
        return v1


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

    def print(self, out_file):
        self.relational.print(out_file)

        if self.alternative == 2:
            out_file.write(" == ")
            self.equality.print(out_file)
        elif self.alternative == 3:
            out_file.write(" != ")
            self.equality.print(out_file)

    def execute(self, values, types):
        v1 = self.relational.execute(values, types)
        if self.alternative in [2, 3]:
            v2 = self.equality.execute(values, types)
            if self.alternative == 2:
                return v1 == v2
            elif self.alternative == 3:
                return v1 != v2
        return v1


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
            self.relational.parse()
            self.alternative = 2
        elif token == Tokenizer.symbols[">="]:
            tk.skip_token()
            self.relational = Relational(tk)
            self.relational.parse()
            self.alternative = 3
        elif token == Tokenizer.symbols["<"]:
            tk.skip_token()
            self.relational = Relational(tk)
            self.relational.parse()
            self.alternative = 4
        elif token == Tokenizer.symbols["<="]:
            tk.skip_token()
            self.relational = Relational(tk)
            self.relational.parse()
            self.alternative = 5

    def print(self, out_file):
        self.additive.print(out_file)

        if self.alternative != 1:
            match self.alternative:
                case 2:
                    out_file.write(" > ")
                case 3:
                    out_file.write(" >= ")
                case 4:
                    out_file.write(" < ")
                case 5:
                    out_file.write(" <= ")

            self.relational.print(out_file)

    def execute(self, values, types):
        v1 = self.additive.execute(values, types)

        if self.alternative in [2, 3, 4, 5]:
            v2 = self.relational.execute(values, types)
            if self.alternative == 2:
                return v1 > v2
            elif self.alternative == 3:
                return v1 >= v2
            elif self.alternative == 4:
                return v1 < v2
            elif self.alternative == 5:
                return v1 <= v2
        return v1


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
            tk.skip_token()
            self.alternative = 2
            self.additive = Additive(tk)
            self.additive.parse()

        elif token == Tokenizer.symbols["-"]:
            tk.skip_token()
            self.alternative = 3
            self.additive = Additive(tk)
            self.additive.parse()

    def print(self, out_file):
        self.multiplicitive.print(out_file)

        if self.alternative == 2:
            out_file.write(" + ")
            self.additive.print(out_file)
        elif self.alternative == 3:
            out_file.write(" - ")
            self.additive.print(out_file)

    def execute(self, values, types):
        v1 = self.multiplicitive.execute(values, types)
        if self.alternative in [2, 3]:
            v2 = self.additive.execute(values, types)
            if self.alternative == 2:
                return v1 + v2
            elif self.alternative == 3:
                return v1 - v2
        return v1


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
            self.alternative = 3
            tk.skip_token()
            self.multiplicitive = Multiplicitive(tk)
            self.multiplicitive.parse()
        elif token == Tokenizer.symbols["%"]:
            self.alternative = 4
            tk.skip_token()
            self.multiplicitive = Multiplicitive(tk)
            self.multiplicitive.parse()
        elif token == Tokenizer.symbols["~"]:
            self.alternative = 5
            tk.skip_token()
            self.multiplicitive = Multiplicitive(tk)
            self.multiplicitive.parse()

    def print(self, out_file):
        self.exponential.print(out_file)

        match self.alternative:
            case 2:
                out_file.write(" * ")
                self.multiplicitive.print(out_file)
            case 3:
                out_file.write(" / ")
                self.multiplicitive.print(out_file)
            case 4:
                out_file.write(" % ")
                self.multiplicitive.print(out_file)
            case 5:
                out_file.write(" ~ ")
                self.multiplicitive.print(out_file)

    def execute(self, values, types):
        v1 = self.exponential.execute(values, types)
        if self.alternative in [2, 3, 4, 5]:
            v2 = self.multiplicitive.execute(values, types)
            if self.alternative == 2:
                return v1 * v2
            elif self.alternative == 3:
                return v1 / v2
            elif self.alternative == 4:
                return v1 % v2
            elif self.alternative == 5:
                return v1 // v2
        return v1


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

    def print(self, out_file):
        self.unary.print(out_file)

        if self.alternative == 2:
            out_file.write(" ^ ")
            self.exponential.print(out_file)

        elif self.alternative == 3:
            out_file.write(" : ")
            self.exponential.print(out_file)

    def execute(self, values, types):
        v1 = self.unary.execute(values, types)
        if self.alternative in [2, 3]:
            v2 = self.exponential.execute(values, types)
            if self.alternative == 2:
                return v1**v2
            elif self.alternative == 3:
                return v1 ** (1 / v2)
        return v1


class Unary:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.postfix = None
        self.term = None
        self.var = None

    def parse(self):
        tk = self.tk
        token = tk.get_token()

        if token == Tokenizer.symbols["++"]:
            self.alternative = 2
            tk.skip_token()
            self.var = Var(tk)
            self.var.parse()
        elif token == Tokenizer.symbols["--"]:
            self.alternative = 3
            tk.skip_token()
            self.var = Var(tk)
            self.var.parse()
        elif token == Tokenizer.symbols["!"]:
            self.alternative = 4
            tk.skip_token()
            self.term = Term(tk)
            self.term.parse()
        else:
            self.alternative = 1
            self.postfix = Postfix(tk)
            self.postfix.parse()

    def print(self, out_file):
        if self.alternative == 1:
            self.postfix.print(out_file)
        elif self.alternative == 2:
            out_file.write("++")
            self.var.print(out_file)
        elif self.alternative == 3:
            out_file.write("--")
            self.var.print(out_file)
        elif self.alternative == 4:
            out_file.write("!")
            self.term.print(out_file)

    def execute(self, values, types):
        if self.alternative == 1:
            return self.postfix.execute(values, types)

        if self.alternative == 4:
            return not self.term.execute(values, types)

        if self.alternative in [2, 3]:
            var = self.var.execute(values, types)
            if var not in values:
                message = f"Prefix operator can only be used on variables."
                raise InvalidOperatorException(message)

            if self.alternative == 2:
                values[var] += 1
                return values[var]
            elif self.alternative == 3:
                values[var] -= 1
                return values[var]


class Postfix:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.alternative = None
        self.term = None
        self.var = None

    def parse(self):
        tk = self.tk

        if tk.get_token() == Tokenizer.name_token:
            self.var = Var(tk)
            self.var.parse()
        else:
            self.alternative = 1
            self.term = Term(tk)
            self.term.parse()

        token = tk.get_token()
        if token == Tokenizer.symbols["++"]:
            self.alternative = 2
            tk.skip_token()

        elif token == Tokenizer.symbols["--"]:
            self.alternative = 3
            tk.skip_token()

    def print(self, out_file):
        if self.alternative == 1:
            self.term.print(out_file)
        else:
            self.var.print(out_file)
        if self.alternative == 2:
            out_file.write("++ ")
        elif self.alternative == 3:
            out_file.write("-- ")

    def execute(self, values, types):
        if self.alternative == 1:
            return self.term.execute(values, types)

        if self.alternative in [2, 3]:
            var = self.var.execute(values, types)
            if var not in values:
                message = f"Postfix operator can only be used on variables."
                raise InvalidOperatorException(message)

            val = values[var]
            if self.alternative == 2:
                values[var] += 1
                return val
            elif self.alternative == 3:
                values[var] -= 1
                return val


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

    def print(self, out_file):
        if self.alternative == 2:
            out_file.write("(")
            self.or_statement.print(out_file)
            out_file.write(")")

        elif self.alternative == 1:
            self.literal.print(out_file)
        elif self.alternative == 3:
            self.var.print(out_file)

    def execute(self, values, types):
        if self.alternative == 1:
            return self.literal.execute(values, types)
        elif self.alternative == 2:
            return self.or_statement.execute(values, types)
        elif self.alternative == 3:
            variable = self.var.execute(values, types)
            return values[variable]


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
            tk.skip_token()
        elif token == Tokenizer.floating_point_token:
            self.type = "float"
            self.value = float(tk.get_literal())
            tk.skip_token()
        elif token == Tokenizer.string_token:
            self.type = "string"
            self.value = tk.get_literal()
            tk.skip_token()
        elif (
            token == Tokenizer.key_words["true"]
            or token == Tokenizer.key_words["false"]
        ):
            self.type = "boolean"
            self.value = token == Tokenizer.key_words["true"]
            tk.skip_token()
        elif token == Tokenizer.symbols["["]:
            self.type = "array"
            array = ArrayLiteral(tk)
            array.parse()
            self.value = array.value
        else:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'literal' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

    def print(self, out_file):
        quote = ""
        if self.type == "string":
            quote = '"'
        out_file.write(f"{quote}{self.value}{quote}")

    def execute(self, values, types):
        return self.value


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
            if token == Tokenizer.symbols[","]:
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
            elif token == Tokenizer.integer_token:
                self.value.append(int(tk.get_literal()))
            elif token == Tokenizer.floating_point_token:
                self.value.append(float(tk.get_literal()))
            else:
                self.value.append(tk.get_literal())

            tk.skip_token()
            token = tk.get_token()
        tk.skip_token()

    def execute(self, values, types):
        return self.value


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

        if token != Tokenizer.name_token:
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

    def print(self, out_file):
        out_file.write(f"{self.name}")

        if self.alternative == 2:
            self.array_access.print(out_file)
        elif self.alternative == 3:
            self.function_call.print(out_file)

    def execute(self, values, name):
        if self.alternative == 2:
            return self.array_access.execute()
        elif self.alternative == 3:
            return self.function_call.execute()
        elif self.alternative == 3:
            return self.name


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

        tk.skip_token()

    def print(self, out_file):
        out_file.write("(")
        for i, exp in enumerate(self.expressions):
            exp.print(out_file)
            if i != len(self.expressions) - 1:
                out_file.write(", ")
        out_file.write(")")

    def execute(self, values, types):
        vals = []
        for expression in self.expressions:
            vals.append(expression.execute(values, types))
        return Program.functions[self.name].execute(vals)


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

    def print(self, out_file):
        out_file.write("[")
        self.or_expression.print(out_file)
        out_file.write("]")

    def execute(self, values, types):
        if Program.type_check(values[self.name], var):
            index = self.or_expression.execute(values, types)
            return values[self.name][index]
        else:
            message = f"Cannot acces type {types[self.name]}."
            raise TypeMismatchException(message)

    def get_name_index(self, values, types):
        return self.name, self.or_expression.execute(values, types)


class Assignment:
    def __init__(self, tk: Tokenizer):
        self.tk = tk
        self.left = None
        self.operator = None
        self.or_expression = None

    def parse(self):
        tk = self.tk

        token = tk.get_token()
        if token != Tokenizer.key_words["let"]:
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'let' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)
        tk.skip_token()

        self.left = Left(tk)
        self.left.parse()

        token = tk.get_token()
        if (
            token < Tokenizer.symbols["*="]
            or token > Tokenizer.symbols[":="]
            and token != Tokenizer.symbols["="]
        ):
            message = f"Incorrect token found on line {tk.get_line_number()}. Expected 'assignment operator' found '{tk.get_literal()}'."
            raise IncorrectTokenException(message)

        self.operator = tk.get_literal()
        tk.skip_token()

        self.or_expression = Or(tk)
        self.or_expression.parse()

    def print(self, out_file):
        out_file.write("let ")
        self.left.print(out_file)
        out_file.write(f" {self.operator} ")
        self.or_expression.print(out_file)

    def execute(self, values, types):

        val = self.or_expression.execute(values, types)
        self.left.execute(values, types, self.operator, val)
        return val


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

    def print(self, out_file):
        out_file.write(self.name)
        if self.alternative == 2:
            self.array_access.print(out_file)

    def execute(self, values, types, operator, set_val):
        if self.alternative == 2:
            arr, index = self.array_access.get_name_index(values, types)
            match operator:
                case "=":
                    values[arr][index] = set_val
                case "*=":
                    values[arr][index] *= set_val
                case "-=":
                    values[arr][index] -= set_val
                case "+=":
                    values[arr][index] += set_val
                case "/=":
                    values[arr][index] /= set_val
                case "~=":
                    values[arr][index] //= set_val

        if self.alternative == 3:
            match operator:
                case "=":
                    values[self.name] = set_val
                case "*=":
                    values[self.name] *= set_val
                case "-=":
                    values[self.name] -= set_val
                case "+=":
                    values[self.name] += set_val
                case "/=":
                    values[self.name] /= set_val
                case "~=":
                    values[self.name] //= set_val


class DuplicateFunctionException(Exception):
    def __init__(self, message):
        super().__init__(message)


class IncorrectTokenException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ArgumentParameterMismatchException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TypeMismatchException(Exception):
    def __init__(self, message):
        super().__init__(message)


class DuplicateVariableException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UndeclaredVariableException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidOperatorException(Exception):
    def __init__(self, message):
        super().__init__(message)
