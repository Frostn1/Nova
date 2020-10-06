from sys import *
ERROR_NAME = "Goblin"
COMPILER_NAME = "Commander"
class Var:

    def __init__(self,name,carry):
        self.name = name
        self.carry = carry
        self.type = self.get_type(carry)

    def get_type(self,carry):
        try:
            if isinstance(carry,str):
                return str
            elif "." in carry:
                return float
            else:
                return int
        except:
            return int
    def get_carry(self):
        return self.carry

class Lexer:
    def __init__(self,text):
        self.text = text
        self.current_letter = text[0][0]
        self.toke = self.current_letter
        self.counter = 0
        self.line_counter = 0
        self.key_words = [
            "typeln(",
            "type(",
            "var",
            "get("
        ]
        self.tokens = [[]]
        self.varss = {}
    def run(self):
        for line in self.text:
            self.tokens.append([]) 
            print(self.tokens)
            for letter in line:
                self.advance()
                self.check_toke()

    def advance(self):
        self.counter += 1
        if self.line_counter < len(self.text)-1:
            if self.counter >= len(self.text[self.line_counter]):
                self.line_counter += 1
                self.current_letter = self.text[self.line_counter][0] 
                self.counter = 0
                self.toke = ""
            else:
                self.current_letter = self.text[self.line_counter][self.counter]
            self.toke += self.current_letter
        else:
            if self.counter < len(self.text[self.line_counter]):
                self.current_letter = self.text[self.line_counter][self.counter]
                self.toke += self.current_letter

    def check_toke(self):
        # print(self.tokens)
        # print(self.line_counter)
        for toke in self.key_words:
            if self.toke == toke:
                self.tokens[self.line_counter-1].append(self.toke)
                self.toke = ""
                return self.tokens
        if self.toke == " ":
            self.toke = ""
            return self.tokens
        if self.toke in self.varss:
            self.tokens[self.line_counter-1].append("VAR;"+self.toke)
            self.toke = ""
            return self.tokens
        if self.toke[0] == '"' and self.toke[len(self.toke)-1] == '"' and len(self.toke) > 1:
            self.tokens[self.line_counter-1].append("STR;"+self.toke.replace('"',""))
            self.toke = ""
            return self.tokens
        return self.tokens
        
        

def check_file(file_t):
    file_ender = file_t[file_t.index(".")+1:]
    if file_ender == "eclip":
        pass
    else:
        print(ERROR_NAME,"Error: Wrong file type given to the",COMPILER_NAME)
        exit(0)

def read_file(file_t):
    with open(file_t) as file1:
        text = file1.readlines()
        new_text = []
        for letter in text:
            if letter[len(letter)-1] == "\n":
                letter = letter[:len(letter)-1]
            new_text.append(letter)
        return new_text
def lex(text):
    lexer_t = Lexer(text)
    # print(len(text))
    
    lexer_t.run()
    print(lexer_t.tokens)

    
            
    # print(lexer_t.current_letter)
    # lexer_t.advance()
    # print(lexer_t.current_letter,lexer_t.toke)
    # print(text)
def run(file_to_run):
    
    check_file(file_to_run)
    lex(read_file(file_to_run))
    
    # varss = {}
    # var_name = "age"
    # varss[var_name] = var(var_name,16)
    # var_name = "name"
    # varss[var_name] = var(var_name,"Sean")
    # for key in varss.keys():
    #     print(varss[key].name,varss[key].carry,varss[key].type)
    # var("age","16")
    
    
    
    
if __name__ == "__main__":
    run(argv[1])




    