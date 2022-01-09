import sys
import lexer

def main(argv : list):
    if len(argv) < 2:
        print('<>')
        lex : lexer.Lexer
        par : lexer.Parser
        sem : lexer.Semantic
        variables_ = {}
        src = ''
        while src != 'hlt':
            src = input("=> ")
            if src != 'hlt':
                lex = lexer.Lexer(src).lexify()
                par = lexer.Parser(lex.tokens, lex.handler)
                par.parse()
                sem = lexer.Semantic(par.tokens, par.handler)
                sem.variables = variables_
                errorFlag = False
                try:
                    sem.analyse()
                except EOFError as e:
                    errorFlag = True
                
                gen = lexer.CodeGen(sem.tokens, sem.handler, sem)
                if not errorFlag:
                    gen.generate(['-r'])
                else:
                    gen.handler.write()
                variables_ = gen.sem.variables
        # raise Exception("file error : missing file")
    else:
        if argv[1] == "" :
            raise Exception("file error : file path empty")
        with open(argv[1], "r") as fileP:
            if not fileP.readable():
                raise Exception("file error : file not readable")
            fileContent = fileP.read()
            if len(argv) > 1:
                flagList = argv[2:]
            lex = lexer.Lexer(fileContent, argv[1], fileP).lexify()
            par = lexer.Parser(lex.tokens, lex.handler)
            par.parse()
            sem = lexer.Semantic(par.tokens, par.handler)
            errorFlag = False
            try:
                sem.analyse()
            except EOFError as e:
                errorFlag = True
            
            gen = lexer.CodeGen(sem.tokens, sem.handler, sem)
            if not errorFlag:
                gen.generate(flagList)
            else:
                gen.handler.write()
        
        
if __name__ == "__main__":
    main(sys.argv)