import sys
import lexer

def runCode(rawCode : str, varia = {}, path = "", pointer = "", flags=['-r']):
    lex : lexer.Lexer
    par : lexer.Parser
    sem : lexer.Semantic
    variables_ = varia
    lex = lexer.Lexer(fileContent=rawCode,filePath=path, filePointer=pointer).lexify()
    par = lexer.Parser(lex.tokens, lex.handler)
    par.parse()
    if len(par.handler.errorList) > 0:
        print("Unknown Error while parsing exprerssion")
        par.handler.write()
    sem = lexer.Semantic(par.tokens, par.handler)
    sem.variables = variables_
    errorFlag = False
    try:
        sem.analyse()
    except EOFError as e:
        errorFlag = True
    
    gen = lexer.CodeGen(sem.tokens, sem.handler, sem)
    if not errorFlag:
        gen.generate(flags)
    else:
        gen.handler.write()
    variables_ = gen.sem.variables



def main(argv : list):
    if len(argv) < 2:
        print('<>')
        variables_ = {}
        src = ''
        while src != 'hlt':
            src = input("=> ")
            if src != 'hlt':
                runCode(src, variables_)
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
            runCode(rawCode=fileContent, path=argv[1], pointer=fileP, flags=flagList)
        
        
if __name__ == "__main__":
    main(sys.argv)