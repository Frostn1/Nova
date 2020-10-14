from sys import *
import os
import Lexer
import Parser
ERROR_NAME = "Goblin"
COMPILER_NAME = "Commander"

LINKED_VAR_NAME = "link"
REGULAR_VAR_NAME = "var"

def check_file(file_t):

    file_ender = file_t[file_t.index(".")+1:]
    if file_ender == "eclip":
        pass
    else:  
        raise Exception (ERROR_NAME+" Error: Wrong file type given to the "+COMPILER_NAME)
        

def read_file(file_t):

    with open(file_t) as file1:
        text = file1.readlines()
        new_text = []
        final_text = []
        for letter in text:
            if letter[len(letter)-1] == "\n":
                letter = letter[:len(letter)-1]
            new_text.append(letter)
        if new_text == []:
            raise Exception(ERROR_NAME+" Error: File is empty")
        for line in new_text:
            if len(line) >= 1:
                final_text.append(line)
        
        return final_text

def lex(text):
    lexer_t = Lexer.Lexer(text) 
    lexer_t.run()
    print(lexer_t.tokens)
    return lexer_t.tokens, lexer_t.varss, lexer_t.vectors,lexer_t.semi_vars

def parse(tokens,varss,vectors,semi):
    parser_t = Parser.Parser(tokens,varss,semi)
    parser_t.run()
def run(file_to_run):
    
    check_file(file_to_run)
    tokens,varss,vectors,semi = lex(read_file(file_to_run))
    
    # print(varss)
    # for var in varss.keys():
    #     print("HMMM",varss[var].name,varss[var].carry,varss[var].type)
    # for key in vectors.keys():
    #     print("HMM",key,vectors[key])
    parse(tokens,varss,vectors,semi)
    

if __name__ == "__main__":
    run(argv[1])