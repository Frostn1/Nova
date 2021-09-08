class Token:
    def __init__(self, _id : int, value : str, line : int, column : int):
        self.id = _id
        self.value = value
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, fileContent : str, filePath = "", filePointer  = ""):
        self.code = fileContent
        self.filePath = filePath
        self.filePointer = filePointer
        self.check = ""
        #-------------------------------

        self.symbols = ['{', '}', '(', ')', '[', ']', '.', '"', '*', '\n', ':', ',',';'] # single-char keywords
        self.other_symbols = ['\\', '/*', '*/'] # multi-char keywords
        self.arthemic = ['=','+','-','*','/']
        self.KEYWORDS = self.symbols + self.other_symbols + self.arthemic

        #-------------------------------

        self.tokens = []
        self.line = 1
        self.column = 1
        self.id = 1
    def addLetter(self, currentChar : chr):
        self.check += currentChar
    def lexify(self):
        length = len(self.code)
        white_space = ' '
        lexeme = ''
        for index,char in enumerate(self.code):
            self.addLetter(char)
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
                        self.tokens.append(Token(self.id, lexeme.replace('\n',''), self.line, self.column-len(lexeme) + 1))
                        self.id += 1
                        lexeme = ''
                else:
                    self.column += 1
            else:
                if lexeme != '':
                    if '\n' in lexeme:
                        self.line += 1
                        self.column = 1
                    elif '\n' not in lexeme:
                        self.column += 1
                    self.tokens.append(Token(self.id, lexeme.replace('\n',''), self.line, self.column-len(lexeme) + 1))
                    self.id += 1
                    lexeme = ''
        return self
    def printTokens(self):
        print("[Check] =>",self.check)
        for token in self.tokens:
            print("[ TOKEN ] -> \n\tvalue :",token.value,"\n\tline :",token.line,"\n\tcolumn :",token.column)


class Parser:
    def __init__(self,lex : Lexer):
        self.tokens = lex.tokens
    
    def parse(self):
        index = 0
        while index < len(self.tokens):
            if self.tokens[index].value == 'let' or self.tokens[index].value == 'link':
                index += 1
                if self.tokens[index].value.isidentifier():
                    index += 1
                    if self.tokens[index].value == '=':
                        index += 1
                        expression = []
                        while self.tokens[index].value != ';':
                            expression.append(self.tokens[index].value)
                            index += 1
                        if len(expression) < 1:
                            print("parser error : missing expression at",self.tokens[index].line,self.tokens[index].column)
                            exit(1)
                        # Check for value or expression
                    else :
                        print("parser error : missing assignment operator at",self.tokens[index].line,self.tokens[index].column)
                        exit(1)
                else:
                    print("parser error : invalid identifier name at",self.tokens[index].line,self.tokens[index].column,"<>",self.tokens[index].value)
                    exit(1)
            index += 1

class Semantic:
    class Symbol:
        def __init__(self, _type : str, value : str, dependencies = [], pos = ()) -> None:
            self.type = _type
            self.value = value
            self.dependencies = dependencies
            self.pos = pos
    class Variable:
        def __init__(self,name : str, value : str, pos : tuple, variables) -> None:
            self.name = name
            self.value = value
            self.pos = pos
            self.type = self.getType(variables)
        def getType(self, _vars):
            if self.value.isnumeric():
                self.type = "number"
            elif self.value.identifier():
                self.type = _vars[self.value].type
            return self.type
    def __init__(self, par : Parser):
        self.tokens = par.tokens
        self.variables = {}
        #-------------------------------------------------

        self.validOperators = [i for i in '+-*/()']
    def checkExpression(self, expressionList : list):
        verified = []
        for index, exp in enumerate(expressionList):
            if exp.isnumeric():
                verified.append(self.Symbol("number", exp, [], (self.tokens[self.index].line, self.tokens[self.index].column)))
            elif exp.isidentifier():
                verified.append(self.Symbol("identifier",exp, [], (self.tokens[self.index].line, self.tokens[self.index].column)))
            elif len(exp) == 1 and exp in self.validOperators:
                verified.append(self.Symbol("operator",exp, [expressionList[index + 1], expressionList[index - 1]], (self.tokens[self.index].line, self.tokens[self.index].column)))
            else:
                print("semantic error : miss identified symbol at", self.tokens[self.index].line, self.tokens[self.index].column,"<>",self.tokens[self.index].value)
                exit(1)
        
        if verified[0].type == "operator":
            print("semantic error : first value can't be an operator at",verified[0].pos[0], verified[0].pos[1])
        if verified[0].type == "identifier":
            lastType = self.variables[verified[0].value].type
            print(verified[0].value, [i for i in self.variables], self.variables[verified[0].value].type)
        else:
            lastType = verified[0].type
        stringList = []
        for index,ver in enumerate(verified):
            if ver.type != "identifier" and ver.type != lastType and ver.type != "operator":
                print("semantic error : mismatch type at", ver.pos[0], ver.pos[1], "<>",ver.value)
                exit(1)
            elif ver.type == "identifier" and self.variables[ver.value].type != lastType:
                print("semantic error : mismatch type at", ver.pos[0], ver.pos[1], "<>",ver.value)
                exit(1)
            if ver.type == "identifier":
                stringList.append(self.variables[ver.value].value)
            else:
                stringList.append(ver.value)
        final = eval("".join(stringList))
        return str(final)
        # print("Final answer", final)

    def analyse(self):
        self.index = 0
        while self.index < len(self.tokens):
            if self.tokens[self.index].value == 'let' or self.tokens[self.index].value == 'link':
                self.index += 1
                if self.tokens[self.index].value.isidentifier():
                    self.index += 1
                    if self.tokens[self.index].value == '=':
                        self.index += 1
                        expression = []
                        while self.tokens[self.index].value != ';':
                            # print("index ->",index, self.tokens[index].value)
                            expression.append(self.tokens[self.index].value)
                            self.index += 1
                        if len(expression) < 1:
                            print("parser error : missing expression at",self.tokens[self.index].line,self.tokens[self.index].column)
                            exit(1)
                        finalValue = self.checkExpression(expression)
                        varName = self.tokens[self.index-len(expression)-2].value
                        self.variables[varName] = self.Variable(
                                                    varName, 
                                                    finalValue, 
                                                    (self.tokens[self.index-len(expression)-2].line,  self.tokens[self.index-len(expression)-2].column),
                                                    self.variables)
                        # Check for value or expression
                    else :
                        print("parser error : missing assignment operator at",self.tokens[self.index].line,self.tokens[self.index].column)
                        exit(1)
                else:
                    print("parser error : invalid iden at",self.tokens[self.index].line,self.tokens[self.index].column)
                    exit(1)
            self.index += 1
    

