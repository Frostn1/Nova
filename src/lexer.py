class Token:
    def __init__(self, value : str, line : int, column : int):
        self.value = value
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, fileContent : str, filePath = "", filePointer  = ""):
        self.code = fileContent
        self.filePath = filePath
        self.filePointer = filePointer

        #-------------------------------

        self.symbols = ['{', '}', '(', ')', '[', ']', '.', '"', '*', '\n', ':', ','] # single-char keywords
        self.other_symbols = ['\\', '/*', '*/'] # multi-char keywords
        KEYWORDS = symbols + other_symbols

        #-------------------------------

        self.tokens = []
        self.line = 1
        self.column = 1

    def lexify(self):
        length = len(self.code)
        white_space = ' '
        lexeme = ''
        for index,char in enumerate(self.code):
            if char == '*':
                if self.code[index-1] == '/':
                    lexeme += '/*'
                elif self.code[index+1] == '/':
                    lexeme += '*/'
                else:
                    lexeme += '*'
            elif char == '/':
                if self.code[index+1] != '*' and self.code[index-1] != '*':
                    lexeme += '/'
                else:
                    continue
            else:
                if char != white_space:
                    lexeme += char # adding a char each time
            if (index+1 < length): # prevents error
                if self.code[index+1] == white_space or self.code[index+1] in KEYWORDS or lexeme in KEYWORDS: # if next char == ' '
                    if lexeme != '':
                        print(lexeme.replace('\n', '<newline>'))
                        lexeme = ''

    def printTokens(self):
        for token in tokens:
            print("[ TOKEN ] -> \n\tvalue :",token.value,"\n\tline :",token.line,"\n\tcolumn :",token.column)
