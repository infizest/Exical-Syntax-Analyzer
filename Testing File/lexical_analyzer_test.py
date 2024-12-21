def test_lexical_analyzer():
    code = """
import math
class MyClass:
    def __init__(self):
        self.value = 10
    def my_function(self):
        print("Hello, World!")
    x = 10
    if x > 0:
        print("Positive")
    for i in range(5):
        print(i)
    # Lambda function
    square = lambda x: x * x
    # Dictionary operations
    my_dict = {"a": 1, "b": 2}
    items = my_dict.items()
    """
    
    lexer = LexicalAnalyzer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        __builtins__.print(token)  

test_lexical_analyzer()