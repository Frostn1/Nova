import sys
import lexer

def main(argv : list):
    if len(argv) < 2:
        raise Exception("file error : missing file")
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
        sem.analyse()
        gen = lexer.CodeGen(sem.tokens, sem.handler, sem)
        gen.generate(flagList)
        
        
if __name__ == "__main__":
    main(sys.argv)