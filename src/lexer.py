class Token:
    def __init__(self, id : int, type : str, value : str, line : int, column : int):
        self.id = id
        self.type = type
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
            elif char != white_space:
                lexeme += char # adding a char each time
            if (index + 1 < length): # prevents error
                if self.code[index+1] == white_space or self.code[index+1] in self.KEYWORDS or lexeme in self.KEYWORDS: # if next char == ' '
                    if lexeme != '':
                        if '\n' in lexeme:
                            self.line += 1
                            self.column = 1
                        elif '\n' not in lexeme:
                            self.column += 1
                        self.tokens.append(Token(lexeme.replace('\n',''), self.line, self.column-len(lexeme) + 1))
                        lexeme = ''
                else:
                    self.column += 1

    def printTokens(self):
        for token in self.tokens:
            print("[ TOKEN ] -> \n\tvalue :",token.value,"\n\tline :",token.line,"\n\tcolumn :",token.column)


class Parser:
    def __init__(self,lex : Lexer):
        self.tokens = lex.tokens
    
    def parse(self):
        index = 0
        while index < len(self.tokens):
            if self.tokens[index].value == 'let':
                index += 1
                if self.tokens[index].value.isidentifier():
                    index += 1
                    if self.tokens[index].value == '=':
                        index += 1
                        expression = []
                        while self.tokens[index].value != ';':
                            print("index ->",index, self.tokens[index].value)
                            expression.append(self.tokens[index].value)
                            index += 1
                        if len(expression) < 1:
                            print("parser error : missing expression at",self.tokens[index].line,self.tokens[index].column)
                        
                        # Check for value or expression
                    else :
                        print("parser error : missing assignment operator at",self.tokens[index].line,self.tokens[index].column)
                else:
                    print("parser error : invalid iden at",self.tokens[index].line,self.tokens[index].column)
                    exit(1)
            index += 1
    

