import re
import json

class LexicalAnalyzer:
    def __init__(self, code):
        self.code = code

    def tokenize(self):
        tokens = {
            'IMPORT': r'\bimport\b',
            'CLASS': r'\bclass\b', 
            'DEF': r'\bdef\b',
            'IF': r'\bif\b',
            'FOR': r'\bfor\b',
            'PRINT': r'\bprint\b',
            'LAMBDA': r'\blambda\b',
            'DICT_METHOD': r'\.(items|values|keys)\(\)', 
            'EXTENDED_OPERAND': r'(\*\*=|^=|%=|//=)',  
            'ASSIGN': r'=',
            'COLON': r':',
            'NUMBER': r'\b\d+\b',
            'STRING': r'"[^"]*"|\'[^\']*\'',
            'COMMENT': r'#.*|""".*?"""',
            'WHITESPACE': r'\s+',
            'NEWLINE': r'\n',
            'VARIABLE': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'DOT': r'\.', 
            'LPAREN': r'\(',  
            'RPAREN': r'\)',  
            'COMPARISON_OPERATOR': r'(\>|\<|\=\=|\!=)',
            'ARITHMETIC_OPERATOR': r'(\+|\-|\*|\/)', 
            'LBRACE': r'\{',  
            'RBRACE': r'\}',  
            'OTHER': r'.' , 
            'DICT_INIT': r'\{[^{}]*\}',  
            'LAMBDA_OP': r'(\|\|)'
        }
        
        pos = 0
        tokens_list = []
        while pos < len(self.code):
            match = None
            for token_type, pattern in tokens.items():
                regex = re.compile(pattern)
                match = regex.match(self.code, pos)
                if match:
                    if token_type != 'WHITESPACE': 
                        tokens_list.append((token_type, match.group()))
                    pos = match.end()
                    break
            if not match:
                raise SyntaxError(f"Illegal character: {self.code[pos]}")
        
        # Save the token list to a file
        with open("token_report.json", "w") as f:
            json.dump(tokens_list, f, indent=4)
        
        return tokens_list

# Test the lexical analyzer
if __name__ == "__main__":
    code = '''
    import math
    class MyClass:
        def my_method(self):
            if x > 0:
                print("Hello World")
            for i in range(5):
                print(i)
    '''
    
    lexer = LexicalAnalyzer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
