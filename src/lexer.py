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
        self.arthemic = ['=','+','-','*','/']
        self.KEYWORDS = self.symbols + self.other_symbols + self.arthemic

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
            elif char != white_space and char != '\n':
                lexeme += char # adding a char each time
            if (index+1 < length): # prevents error
                if self.code[index+1] == white_space or self.code[index+1] in self.KEYWORDS or lexeme in self.KEYWORDS: # if next char == ' '
                    if lexeme != '':
                        self.tokens.append(Token(lexeme, self.line, self.column-len(lexeme) + 1))
                        if '\n' in lexeme:
                            self.line += 1
                            self.column = 1
                        else:
                            self.column += 1
                        lexeme = ''
                else:
                    self.column += 1

    def printTokens(self):
        for token in self.tokens:
            print("[ TOKEN ] -> \n\tvalue :",token.value,"\n\tline :",token.line,"\n\tcolumn :",token.column)
