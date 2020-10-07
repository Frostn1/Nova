from sys import *
import os
ERROR_NAME = "Goblin"
COMPILER_NAME = "Commander"
class Var:

    def __init__(self,name,carry):
        self.name = name
        self.carry = carry
        # self.type = self.get_type(carry)

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
            
            
            for letter in line:
                self.advance()
                check = self.check_toke()
                if check == "con":
                    
                    break
            self.tokens.append([]) 
           

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
    def check_sign(self,toke):
        self.sign_list = ["+","-","*","/","^","(",")"]
        for sign in self.sign_list:
            if sign == toke:
                return sign
        return False

    def check_toke(self):

        for toke in self.key_words:
        
            if self.toke == toke:
                print(toke,self.line_counter)
                self.tokens[len(self.tokens)-1].append(self.toke)
                self.toke = ""
                return self.tokens
        if self.toke == " ":
            self.toke = ""
            return self.tokens
        if self.toke in self.varss.keys():
            self.tokens[len(self.tokens)-1].append("VAR;"+self.toke)
            self.toke = ""
            return self.tokens
        if self.toke[0] == '"' and self.toke[len(self.toke)-1] == '"' and len(self.toke) > 1:
            self.tokens[len(self.tokens)-1].append("STR;"+self.toke.replace('"',""))
            self.toke = ""
            return self.tokens
        
        if self.current_letter == "+" or self.counter == len(self.text[self.line_counter])-1 and self.toke[:-1].replace(".","").isnumeric():
            if "." in self.toke:
                self.tokens[len(self.tokens)-1].append("FLOAT;"+self.toke.replace(")",""))
            else:
                self.tokens[len(self.tokens)-1].append("INT;"+self.toke.replace(")",""))
            return self.tokens

        #Create a Var section
        try:

            if self.tokens[self.line_counter][0] == "var":

                var_t_name = self.text[self.line_counter][self.text[self.line_counter].index("var")+4:].split("=")[0][:-1]
                var_t_carry = self.text[self.line_counter][self.text[self.line_counter].index("var")+4:].split("=")[1][1:]
                toke_t = ""
                var_t_tokens = []
                counter_t = 0
                #Name Checking:
                if var_t_name in self.varss.keys():
                    raise Exception (ERROR_NAME+" Error: Var name '"+var_t_name+"',Has been manufactored before and can not again")
                
                for letter in var_t_carry:
                    toke_t += letter
                    counter_t += 1 
                   
                    if toke_t == " ":
                        toke_t = ""
                    elif self.check_sign(letter) or counter_t == len(var_t_carry):
                        
                        if toke_t[:-1].replace(" ","").count(".") == 1:
                            if self.check_sign(toke_t[-1]):
                                var_t_tokens.append("FLOAT;"+toke_t[:-1].replace(" ",""))
                            else:
                                var_t_tokens.append("FLOAT;"+toke_t.replace(" ",""))
                            
                        elif toke_t[:-1].replace(" ","").isnumeric():
                            if self.check_sign(toke_t[-1]):
                                var_t_tokens.append("INT;"+toke_t[:-1].replace(" ",""))
                            else:
                                var_t_tokens.append("INT;"+toke_t.replace(" ",""))
                        if self.check_sign(toke_t[-1]):
                            var_t_tokens.append(toke_t[-1])
                        toke_t = ""
                self.varss[var_t_name] = Var(var_t_name,var_t_tokens)
                self.tokens[len(self.tokens)-1].append(var_t_name)
                    
                # print("BLA",var_t_tokens)
                
                self.toke = ""
                
                return "con"
                
        except:
            
            pass
        return self.tokens
        
        

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
        for letter in text:
            if letter[len(letter)-1] == "\n":
                letter = letter[:len(letter)-1]
            new_text.append(letter)
        return new_text
def lex(text):
    lexer_t = Lexer(text)
    # print(len(text))
    
    lexer_t.run()
    
    for key in lexer_t.varss.keys():
        print(lexer_t.varss[key].name,lexer_t.varss[key].carry)
    
    # print(lexer_t.varss)
    print(lexer_t.tokens)

    
            
    # print(lexer_t.current_letter)
    # lexer_t.advance()
    # print(lexer_t.current_letter,lexer_t.toke)
    # print(text)
def run(file_to_run):
    
    check_file(file_to_run)
    lex(read_file(file_to_run))
    
    
    
    
    
    
if __name__ == "__main__":
    run(argv[1])




    