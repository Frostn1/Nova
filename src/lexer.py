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
        
        #----------------------------------

        self.functionState = 0
        self.currentFunction = ""
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
                        while index < len(self.tokens) and self.tokens[index].value != ';':
                            expression.append(self.tokens[index].value)
                            index += 1
                        if len(expression) < 1:
                            self.handler.add(errorhandling.Error("parser", "syntax", "missing expression", (self.tokens[index].line,self.tokens[index].column)))
                    else :
                        self.handler.add(errorhandling.Error("parser", "syntax", "missing assignment operator at", (self.tokens[index].line,self.tokens[index].column)))
                        
                else:
                    self.handler.add(errorhandling.Error("parser", "naming", "invalid identifier name", (self.tokens[index].line,self.tokens[index].column)))
            elif self.tokens[index].value == 'fn':
                index += 1
                if self.tokens[index].value.isidentifier():
                    index += 1
                    if self.tokens[index].value == '(':
                        index += 1
                        args = []
                        while self.tokens[index].value != ')' and self.tokens[index].value != '{':
                            if self.tokens[index].value != ',':
                                args.append(self.tokens[index].value)
                            index += 1
                        if self.tokens[index].value == '{':
                            self.handler.add(errorhandling.Error("parser", "syntax", "missing closing on function define", (self.tokens[index].line,self.tokens[index].column)), ')')
                        else :
                            index += 1
                            for arg in args:
                                if not arg.isidentifier():
                                    self.handler.add(errorhandling.Error("parser", "naming", "invalid identifier name", (self.tokens[index].line,self.tokens[index].column)), arg)
                            self.functionState += 1
            elif self.tokens[index].value == '}' and not self.functionState:
                self.handler.add(errorhandling.Error("parser", "syntax", "unexpected char", (self.tokens[index].line,self.tokens[index].column)), "}")
            elif self.tokens[index].value.isidentifier():
                index += 1
                if self.tokens[index].value == '=':
                    index += 1
                    expression = []
                    while index < len(self.tokens) and self.tokens[index].value != ';':
                        expression.append(self.tokens[index].value)
                        index += 1
                    if len(expression) < 1:
                        self.handler.add(errorhandling.Error("parser", "syntax", "missing expression", (self.tokens[index].line,self.tokens[index].column)))
                else :
                        self.handler.add(errorhandling.Error("parser", "syntax", "missing assignment operator at", (self.tokens[index].line,self.tokens[index].column)))
                        
            else:
                self.handler.add(errorhandling.Error("parser", "syntax", "unexpected token", (self.tokens[index].line,self.tokens[index].column)))
                
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
            self.type = ""
            self.getType(variables)
        def getType(self, _vars):
            if self.value.isnumeric():
                self.type = "number"
            elif self.value.isidentifier():
                self.type = _vars[self.value].type

    class Function(Variable):
        def __init__(self, name: str, value: str, pos: tuple, variables, index, args) -> None:
            super().__init__(name, "0", pos, variables)
            self.name = name
            self.args = args
            self.tokens = []
            self.index = index
            # super(type(),self).__init__(name, "0", pos, variables)
    def __init__(self, tokens, handler):
        self.tokens = tokens
        self.variables = {}
        self.functions = {}
        self.handler = handler

        #-------------------------------------------------

        self.validOperators = [i for i in '+-*/']
        self.brackets = [i for i in '()']

        #-------------------------------------------------
        
        self.index = 0
        self.functionState = 0
        self.currentFunction = ""

    def checkExpression(self, expressionList : list):
        verified = []
        for index, exp in enumerate(expressionList):
            if exp.isnumeric() or ('.' in exp and exp[exp.index('.')+1:].isnumeric() and exp[:exp.index('.')].isnumeric()):
                verified.append(self.Symbol("number", exp, [], (self.tokens[self.index].line, self.tokens[self.index].column)))
            elif exp.isidentifier():
                verified.append(self.Symbol("identifier",exp, [], (self.tokens[self.index].line, self.tokens[self.index].column)))
            elif len(exp) == 1 and exp in self.validOperators:
                verified.append(self.Symbol("operator",exp, [expressionList[index + 1], expressionList[index - 1]], (self.tokens[self.index].line, self.tokens[self.index].column)))
            elif len(exp) == 1 and exp in self.brackets:
                verified.append(self.Symbol("bracket",exp, [], (self.tokens[self.index].line, self.tokens[self.index].column)))
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
        elif verified[0].type == "bracket":
            i = 1
            while i < len(verified) and verified[i].type != "bracket" and verified[i].type != "operator":
                i += 1
            if verified[i - 1].type == "identifier":
                if verified[i - 1].value in self.variables.keys():
                    lastType = self.variables[verified[i - 1].value].type
                else:
                    self.handler.add(errorhandling.Error("semantic", "naming", "unmatched variable name", (verified[i-1].pos[0], verified[i-1].pos[1]), verified[i-1].value))
                    lastType = "number"
            else:
                lastType = verified[i - 1].type
        else:
            lastType = verified[0].type
        stringList = []
        for index,ver in enumerate(verified):
            try:
                if ver.type != "identifier" and ver.type != lastType and ver.type != "operator" and ver.type != "bracket":
                    self.handler.add(errorhandling.Error("semantic", "types", "missmatch type", (ver.pos[0], ver.pos[1]), ver.value))
                elif ver.type == "identifier" and (ver.value in self.variables.keys() and self.variables[ver.value].type != lastType):
                    self.handler.add(errorhandling.Error("semantic", "types", "mismatch type", (ver.pos[0], ver.pos[1]), ver.value))
                elif ver.type == "identifier" and ver.value not in self.variables.keys():
                    self.handler.add(errorhandling.Error("semantic", "bounds", "variables used before assignment", (ver.pos[0], ver.pos[1]), ver.value))
                elif ver.type == "identifier":
                    stringList.append(self.variables[ver.value].value)
                else:
                    stringList.append(ver.value)
            except UnboundLocalError as e:
                self.handler.add(errorhandling.Error("semantic", "fatal", "variables used before assignment", (ver.pos[0], ver.pos[1]), ver.value))
                raise EOFError()
        final = eval("".join(stringList))
        return str(final)

    def analyse(self):
        while self.index < len(self.tokens):
            if self.tokens[self.index].value == 'let' or self.tokens[self.index].value == 'link':
                self.index += 1
                if self.tokens[self.index].value.isidentifier():
                    self.index += 1
                    if self.tokens[self.index].value == '=':
                        self.index += 1
                        expression = []
                        while self.index < len(self.tokens) and self.tokens[self.index].value != ';':
                            expression.append(self.tokens[self.index].value)
                            self.index += 1
                        if len(expression) < 1:
                            self.handler.add(errorhandling.Error("parser", "syntax", "missing expression", (self.tokens[self.index].line,self.tokens[self.index].column)))

                        finalValue = self.checkExpression(expression)
                        varName = self.tokens[self.index-len(expression)-2].value
                        self.variables[varName] = self.Variable(
                                                    varName, 
                                                    finalValue, 
                                                    (self.tokens[self.index-len(expression)-2].line,  self.tokens[self.index-len(expression)-2].column),
                                                    self.variables)
            elif self.tokens[self.index].value == 'fn':
                self.index += 1
                if self.tokens[self.index].value.isidentifier():
                    self.index += 1
                    if self.tokens[self.index].value == '(':
                        self.index += 1
                        args = []
                        while self.tokens[self.index].value != ')' and self.tokens[self.index].value != '{':
                            if self.tokens[self.index].value != ',':
                                args.append(self.tokens[self.index].value)
                            self.index += 1
                        if self.tokens[self.index].value == '{':
                            self.handler.add(errorhandling.Error("parser", "syntax", "missing closing on function define", (self.tokens[self.index].line,self.tokens[self.index].column), ')'))
                        else :
                            self.index += 1
                            for arg in args:
                                if not arg.isidentifier():
                                    self.handler.add(errorhandling.Error("parser", "naming", "invalid identifier name", (self.tokens[self.index].line,self.tokens[self.index].column), arg))
                            self.index += 1
                            self.functions[self.currentFunction] = self.Function(name=self.currentFunction, args=args, pos=(self.tokens[self.index].line,self.tokens[self.index].column), index=self.index, variables=self.variables, value="09")
                            self.functionState += 1
            elif self.tokens[self.index].value == "return" and self.functionState:
                self.index += 1
                expression = []
                while self.tokens[self.index].value != ';':
                    expression.append(self.tokens[self.index].value)
                    self.index += 1
                if len(expression) < 1:
                    self.handler.add(errorhandling.Error("parser", "syntax", "missing expression", (self.tokens[self.index].line,self.tokens[self.index].column)))
                finalValue = self.checkExpression(expression)
                self.functions[self.currentFunction].value = finalValue
                self.functions[self.currentFunction].getType(self.variables)
            elif self.tokens[self.index].value == '}' and self.functionState:
                self.variables[self.currentFunction] = self.functions[self.currentFunction]
                self.functions[self.currentFunction].tokens = self.tokens[self.functions[self.currentFunction].index:self.index]
                print("Token Check", [i.value for i in self.tokens[self.functions[self.currentFunction].index:self.index]])
                self.functionState -= 1
                self.currentFunction = ""
            elif self.tokens[self.index].value.isidentifier():
                self.index += 1
                if self.tokens[self.index].value == '=':
                    self.index += 1
                    expression = []
                    while self.tokens[self.index].value != ';':
                        expression.append(self.tokens[self.index].value)
                        self.index += 1
                    if len(expression) < 1:
                        self.handler.add(errorhandling.Error("parser", "syntax", "missing expression", (self.tokens[self.index].line,self.tokens[self.index].column)))
                    finalValue = self.checkExpression(expression)
                    varName = self.tokens[self.index-len(expression)-2].value
                    self.variables[varName] = self.Variable(
                                                varName, 
                                                finalValue, 
                                                (self.tokens[self.index-len(expression)-2].line,  self.tokens[self.index-len(expression)-2].column),
                                                self.variables)
                else :
                        self.handler.add(errorhandling.Error("parser", "syntax", "missing assignment operator at", (self.tokens[self.index].line,self.tokens[self.index].column)))
                        
            else:
                self.handler.add(errorhandling.Error("parser", "naming", "invalid identifier name", (self.tokens[self.index].line,self.tokens[self.index].column)))
            self.index += 1
    

class CodeGen:
    class Flag:
        def __init__(self, shortname, longname) -> None:
            self.shortname = shortname
            self.longname = longname
            self.used = False
    def __init__(self, tokens, handler, sem, filepath = 'default.c') -> None:
        self.tokens = tokens
        self.handler = handler
        self.filepath = filepath
        self.sem = sem
        self.sem.index = 0
    
    def generate(self, flags : list) -> None:
        flagChecks = [self.Flag("cf","cformat"),self.Flag("le","logerrors"),self.Flag("pf","printfunctions"),self.Flag("e","export")]
        for flag in flags:
            if flag[0] != '-' or len(flag) - flag.count('-') < 1:
                self.handler.add(errorhandling.Error("generator", "syntax", "unexpected flag at CLI",(0,0),flag))
            elif (flag[2:] == flagChecks[1].longname or flag[1:] == flagChecks[1].shortname) and not flagChecks[1].used:
                flagChecks[1].used = True
                self.handler.write()
            elif (flag[2:] == flagChecks[0].longname or flag[1:] == flagChecks[0].shortname) and not flagChecks[0].used:
                flagChecks[0].used = True
                self.cgenrate()
            elif (flag[2:] == flagChecks[2].longname or flag[1:] == flagChecks[2].shortname) and not flagChecks[2].used:
                flagChecks[2].used = True
                print("-pf flag")
            elif (flag[2:] == flagChecks[3].longname or flag[1:] == flagChecks[3].shortname) and not flagChecks[3].used:
                flagChecks[3].used = True
                print("-e flag")

    def cgenrate(self):
        def guesstype(expression):
            exp = self.sem.checkExpression(expression)
            if exp.isnumeric() or ('.' in exp and exp[exp.index('.')+1:].isnumeric() and exp[:exp.index('.')].isnumeric() and exp[:exp.index('.')][0] == '0'):
                return 'int'
            elif ('.' in exp and exp[exp.index('.')+1:].isnumeric() and exp[:exp.index('.')].isnumeric()):
                return 'float'

        def newfile(path, includes = []):
            with open(path, 'w') as new:
                formalIncludes = ['stdio.h','stdlib.h', 'string.h']
                formalIncludes += includes
                for include in formalIncludes:
                    new.write('#include <'+include+'>\n')
                new.write('\nint main(int argc, char** argv) {\n')
        newfile(self.filepath)
        with open(self.filepath,'a') as new:
            index = 0
            while index < len(self.tokens):
                if self.tokens[index].value == 'let':
                    index += 3
                    expression = []
                    while index < len(self.tokens) - 1 and self.tokens[index].value != ';':   
                        expression.append(self.tokens[index].value)
                        index += 1
                    new.write('\t' + guesstype(expression))
                    new.write(' ' +  self.tokens[index-len(expression) - 2].value)
                    new.write(' ' + self.tokens[index-len(expression) - 1].value)
                    new.write(' ' + ' '.join(expression) + ';\n')
                elif self.tokens[index].value == 'link':
                    index += 3
                    expression = []
                    while index < len(self.tokens) - 1 and self.tokens[index].value != ';':   
                        expression.append(self.tokens[index].value)
                        index += 1
                    print(expression, self.tokens[index-len(expression) - 2].value)
                elif self.tokens[index].value in self.sem.variables.keys():
                    index += 2
                    expression = []
                    while index < len(self.tokens) - 1 and self.tokens[index].value != ';':   
                        expression.append(self.tokens[index].value)
                        index += 1
                    new.write('\t' +  self.tokens[index-len(expression) - 2].value)
                    new.write(' ' + self.tokens[index-len(expression) - 1].value)
                    new.write(' ' + ' '.join(expression) + ';\n')
                index += 1
            new.write('}')
            
                