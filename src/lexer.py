import errorhandling

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

        self.handler = errorhandling.ErrorHandler()
        #-------------------------------

        self.symbols = ['{', '}', '(', ')', '[', ']', '"', '*', '\n', ':', ',',';'] # single-char keywords
        self.other_symbols = ['\\', '/*', '*/'] # multi-char keywords
        self.arthemic = ['=','+','-','*','/']
        self.KEYWORDS = self.symbols + self.other_symbols + self.arthemic

        #-------------------------------

        self.tokens = []
        self.line = 1
        self.column = 1
        self.id = 1
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
                lexeme += char
            if (index + 1 < length):
                if self.code[index+1] == white_space or self.code[index+1] in self.KEYWORDS or lexeme in self.KEYWORDS:
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
        for token in self.tokens:
            print("[ TOKEN ] -> \n\tvalue :",token.value,"\n\tline :",token.line,"\n\tcolumn :",token.column)


class Parser:
    def __init__(self,tokens, handler):
        self.tokens = tokens
        self.handler = handler
        self.tokens = self.removeComments()
        for error in self.handler.errorList:
            print(error)
    def removeComments(self):
        index = 0
        while index < len(self.tokens):
            if index < len(self.tokens) - 1 and self.tokens[index].value + self.tokens[index + 1].value == "//":
                currentLine = self.tokens[index].line
                lineFlag = True
                self.tokens.pop(index)
                self.tokens.pop(index)
                while index < len(self.tokens) and lineFlag:
                    if self.tokens[index].line == currentLine:
                        self.tokens.pop(index)
                    else:
                        lineFlag = False
            if index < len(self.tokens) and self.tokens[index].value == '':
                self.tokens.pop(index)
            else:
                index += 1
        return self.tokens
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
                            self.handler.add(errorhandling.Error("parser", "syntax", "missing expression", (self.tokens[index].line,self.tokens[index].column)))
                            # print("parser error : missing expression at",self.tokens[index].line,self.tokens[index].column)
                            # exit(1)
                        # Check for value or expression
                    else :
                        self.handler.add(errorhandling.Error("parser", "syntax", "missing assignment operator at", (self.tokens[index].line,self.tokens[index].column)))
                        # print("parser error : missing assignment operator at",self.tokens[index].line,self.tokens[index].column)
                        # exit(1)
                else:
                    self.handler.add(errorhandling.Error("parser", "naming", "invalid identifier name", (self.tokens[index].line,self.tokens[index].column)))
                    # print("parser error : invalid identifier name at",self.tokens[index].line,self.tokens[index].column,"<>",self.tokens[index].value)
                    # exit(1)
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
            self.getType(variables)
        def getType(self, _vars):
            if self.value.isnumeric():
                self.type = "number"
            elif self.value.isidentifier():
                self.type = _vars[self.value].type
    def __init__(self, tokens, handler):
        self.tokens = tokens
        self.variables = {}
        self.handler = handler
        #-------------------------------------------------

        self.validOperators = [i for i in '+-*/()']
    def checkExpression(self, expressionList : list):
        verified = []
        for index, exp in enumerate(expressionList):
            if exp.isnumeric() or ('.' in exp and exp[exp.index('.')+1:].isnumeric() and exp[:exp.index('.')].isnumeric()):
                verified.append(self.Symbol("number", exp, [], (self.tokens[self.index].line, self.tokens[self.index].column)))
            elif exp.isidentifier():
                verified.append(self.Symbol("identifier",exp, [], (self.tokens[self.index].line, self.tokens[self.index].column)))
            elif len(exp) == 1 and exp in self.validOperators:
                verified.append(self.Symbol("operator",exp, [expressionList[index + 1], expressionList[index - 1]], (self.tokens[self.index].line, self.tokens[self.index].column)))
            else:
                self.handler.add(errorhandling.Error("semantic", "symbols", "miss identified symbol", (self.tokens[self.index].line, self.tokens[self.index].column), exp))
                # print("semantic error : miss identified symbol at", self.tokens[self.index].line, self.tokens[self.index].column,"<>",exp)
                # exit(1)
        
        if verified[0].type == "operator":
            self.handler.add(errorhandling.Error("semantic", "syntax", "first value can't be an operator", (verified[0].pos[0], verified[0].pos[1]), verified[0].value))
            # print("semantic error : first value can't be an operator at",verified[0].pos[0], verified[0].pos[1])
            # exit(1)
        if verified[0].type == "identifier":
            if verified[0].value in self.variables.keys():
                lastType = self.variables[verified[0].value].type
            else:
                self.handler.add(errorhandling.Error("semantic", "naming", "unmatched variable name", (verified[0].pos[0], verified[0].pos[1]), verified[0].value))
                # print("semantic error : unmatched variable name at",verified[0].pos[0],verified[0].pos[1],"<>",verified[0].value)
                # exit(1)
        else:
            lastType = verified[0].type
        stringList = []
        for index,ver in enumerate(verified):
            if ver.type != "identifier" and ver.type != lastType and ver.type != "operator":
                self.handler.add(errorhandling.Error("semantic", "types", "mismatch type", (verified[0].pos[0], verified[0].pos[1]), verified[0].value))
                # print("semantic error : mismatch type at", ver.pos[0], ver.pos[1], "<>",ver.value)
                # exit(1)
            elif ver.type == "identifier" and self.variables[ver.value].type != lastType:
                self.handler.add(errorhandling.Error("semantic", "types", "mismatch type", (verified[0].pos[0], verified[0].pos[1]), verified[0].value))
                # print("semantic error : mismatch type at", ver.pos[0], ver.pos[1], "<>",ver.value)
                # exit(1)
            if ver.type == "identifier":
                stringList.append(self.variables[ver.value].value)
            else:
                stringList.append(ver.value)
        final = eval("".join(stringList))
        return str(final)

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
                        
                        finalValue = self.checkExpression(expression)
                        varName = self.tokens[self.index-len(expression)-2].value
                        self.variables[varName] = self.Variable(
                                                    varName, 
                                                    finalValue, 
                                                    (self.tokens[self.index-len(expression)-2].line,  self.tokens[self.index-len(expression)-2].column),
                                                    self.variables)
            self.index += 1
    

class CodeGen:
    def __init__(self, tokens, handler) -> None:
        self.tokens = tokens
        self.handler = handler

    def generate(self, flags : list) -> None:
        for flag in flags:
            if flag[0] != '-':
                self.handler.add(errorhandling.Error("generator", "syntax", "unexpected flag at CLI",(0,0),flag))
        self.handler.write()