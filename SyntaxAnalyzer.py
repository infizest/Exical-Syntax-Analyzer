
class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens  
        self.pos = 0  

    def parse(self):
        try:
            self.program() 
            return "Compilation ended successfully. You just compiled a Python source code!"
        except Exception as e:
            return str(e)

    def program(self):
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'COMMENT':
            self.comment()  

        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'IMPORT':
            self.match('IMPORT')
            self.match('VARIABLE') 
        self.statements()

    def statements(self):
        while self.pos < len(self.tokens):
            self.statement()

    def statement(self):
        token_type = self.tokens[self.pos][0]
        
        if token_type == 'VARIABLE':
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'DOT':
                self.method_call() 
            else:
                self.assignment() 
        elif token_type == 'CLASS':
            self.class_definition()
        elif token_type == 'DEF':
            self.function_definition()
        elif token_type == 'IF':
            self.if_statement()
        elif token_type == 'FOR':
            self.for_loop()
        elif token_type == 'PRINT':
            self.display_message()
        elif token_type == 'LAMBDA':
            self.lambda_expression()
        elif token_type == 'DICT_METHOD':
            self.dictionary_operation()
        elif token_type == 'COMMENT':
            self.comment()
        elif token_type == 'ARITHMETIC_OPERATOR':
            self.arithmetic_expression() 
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")

    def assignment(self):
        self.match('VARIABLE')  
        if self.tokens[self.pos][0] == 'EXTENDED_OPERAND':
            self.match('EXTENDED_OPERAND')
        else:
            self.match('ASSIGN')  # '=' operator

        # Right-hand side can be a VARIABLE, NUMBER, or STRING
        if self.tokens[self.pos][0] in ['VARIABLE', 'NUMBER', 'STRING']:
            self.match(self.tokens[self.pos][0])
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")

    def method_call(self):
        self.match('VARIABLE')  # The object or variable (e.g., my_dict)
        self.match('DOT')  # The dot indicating method call or attribute access
        self.match('VARIABLE')  # The method or attribute name (e.g., items)
        self.match('LPAREN')  # Match the opening '(' for method calls
        self.match('RPAREN')  # Match the closing ')'

    def lambda_expression(self):
        self.match('LAMBDA')
        self.match('VARIABLE')
        self.match('COLON')
        self.expression()  

    def expression(self):
        """Handles an expression which could involve variables, numbers, or operators."""
        self.match(['VARIABLE', 'NUMBER'])  # Match the initial part of the expression
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ['ARITHMETIC_OPERATOR']:
            self.match('ARITHMETIC_OPERATOR')  # Match operators like +, *, etc.
            self.match(['VARIABLE', 'NUMBER'])  # Match the next operand

    def dictionary_operation(self):
        self.match('VARIABLE')
        self.match('DICT_METHOD')

    def arithmetic_expression(self):
        """Handles simple arithmetic expressions, e.g., x * 5"""
        left_operand = self.match('VARIABLE')  # Left operand (e.g., 'x')
        operator = self.match('ARITHMETIC_OPERATOR')  # The operator (e.g., '*')
        right_operand = self.match(['NUMBER', 'VARIABLE'])  # Right operand (e.g., 5 or y)

        # After parsing the operator, we should check if it's part of a more complex expression
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] in ['ARITHMETIC_OPERATOR']:
            # Continue to handle more complex expressions (e.g., x * 5 + 3)
            self.arithmetic_expression()

    def match(self, token_types):
        """Match the current token with the expected token type(s)."""
        if isinstance(token_types, list):
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] in token_types:
                self.pos += 1
            else:
                raise SyntaxError(f"Expected one of {token_types}, found {self.tokens[self.pos]}")
        else:
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == token_types:
                self.pos += 1
            else:
                raise SyntaxError(f"Expected {token_types}, found {self.tokens[self.pos]}")

    def class_definition(self):
        self.match('CLASS')
        self.match('VARIABLE')
        self.match('COLON')

    def function_definition(self):
        self.match('DEF')
        self.match('VARIABLE')
        self.match('LPAREN')  # Match the opening '('
        self.match('VARIABLE')  # Argument, e.g., 'self'
        self.match('RPAREN')  # Match the closing ')'
        self.match('COLON')

    def if_statement(self):
        self.match('IF')
        self.match('VARIABLE')  # Match the variable (e.g., 'x')
        token_type = self.tokens[self.pos][0]
        if token_type == 'COMPARISON_OPERATOR':
            self.match('COMPARISON_OPERATOR')  # Match the comparison operator (e.g., '>')
        else:
            raise SyntaxError(f"Expected comparison operator, found {self.tokens[self.pos]}")
        self.match('NUMBER')  # Match the number on the right side of the comparison
        self.match('COLON')  # Match the colon at the end of the if statement

    def for_loop(self):
        self.match('FOR')
        self.match('VARIABLE')  
        self.match('IN')  # 'IN' keyword
        self.match('VARIABLE')  # function name 
        self.match('LPAREN')  # '('
        self.match('NUMBER')  # range parameter 
        self.match('RPAREN')  # ')'
        self.match('COLON')  

    def display_message(self):
        self.match('PRINT')
        self.match('LPAREN')  # Match the opening '('
        token_type = self.tokens[self.pos][0]
        if token_type == 'STRING':
            self.match('STRING')  # string argument
        elif token_type == 'VARIABLE':
            self.match('VARIABLE')  # variable argument (e.g., 'i')
        else:
            raise SyntaxError(f"Expected STRING or VARIABLE, found {self.tokens[self.pos]}")
        self.match('RPAREN')  # Match the closing ')'

    def comment(self):
        self.match('COMMENT')


# Testing the SyntaxAnalyzer with the sample tokens
tokens = [
    ('IMPORT', 'import'),
    ('VARIABLE', 'math'),
    ('VARIABLE', 'x'),
    ('ASSIGN', '='),
    ('NUMBER', '10'),
    ('IF', 'if'),
    ('VARIABLE', 'x'),
    ('COMPARISON_OPERATOR', '>'),
    ('NUMBER', '0'),
    ('COLON', ':'),
    ('PRINT', 'print'),
    ('LPAREN', '('),
    ('STRING', '"Positive"'),
    ('RPAREN', ')'),
    ('FOR', 'for'),
    ('VARIABLE', 'i'),
    ('IN', 'in'),
    ('VARIABLE', 'range'),
    ('LPAREN', '('),
    ('NUMBER', '5'),
    ('RPAREN', ')'),
    ('COLON', ':'),
    ('PRINT', 'print'),
    ('LPAREN', '('),
    ('VARIABLE', 'i'),
    ('RPAREN', ')'),
    ('DEF', 'def'),
    ('VARIABLE', 'my_function'),
    ('LPAREN', '('),
    ('VARIABLE', 'self'),
    ('RPAREN', ')'),
    ('COLON', ':'),
    ('PRINT', 'print'),
    ('LPAREN', '('),
    ('STRING', '"Hello, World!"'),
    ('RPAREN', ')'),
    ('LAMBDA', 'lambda'),
    ('VARIABLE', 'x'),
    ('COLON', ':'),
    ('VARIABLE', 'x'),
    ('ARITHMETIC_OPERATOR', '*'),
    ('VARIABLE', 'x'),
    ('COMMENT', '# This is a comment')
]

# Create an instance of the SyntaxAnalyzer
analyzer = SyntaxAnalyzer(tokens)

# Parse the tokens and print the result
result = analyzer.parse()
print(result)
