from sys import *
import os
ERROR_NAME = "Goblin"
COMPILER_NAME = "Commander"
class Var:

    def __init__(self,name,carry,type_):
        self.name = name
        self.carry = carry
        self.type = type_
    
    
    def get_type(self):
        return self.type
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
            "connec",
            "get("
        ]

        self.tokens = [[]]
        self.varss = {}
    
    def run(self):

        check = ""
        for line in self.text:  
            for letter in line:
                self.advance()
                if len(self.text[self.line_counter]) > 0:
                    check = self.check_toke()
                if check == "con":
                    self.toke = ""
                    self.line_counter += 1
                    self.counter = -1
                    break
            self.tokens.append([]) 
            check = ""
            
        
           

    def advance(self):
        self.counter += 1
        if self.line_counter < len(self.text)-1:
            if self.counter >= len(self.text[self.line_counter]):
                self.line_counter += 1
                try:
                    self.current_letter = self.text[self.line_counter][0]
                    
                except:
                    pass
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
        self.sign_list = ["+","-","*","/","^","(",")","="]
        for sign in self.sign_list:
            if sign == toke:
                return sign
        return False
    def check_type(self,exp):
        pass
    def calc(self,list_):

        
        sum = []
        for word in list_:

            if "VAR" in word or "CONNEC" in word:
                sum.append(self.calc(self.varss[word[word.index(";")+1:]]))
            else:
                try:
                    sum.append(word[word.index(";")+1:])
                except:
                    sum.append(word)
                    pass
        return sum
    def check_toke(self):
        
        for toke in self.key_words:
            
            if self.toke == toke:
                
                self.tokens[len(self.tokens)-1].append(self.toke)
                self.toke = ""
                return self.tokens

        if self.toke == " ":
            self.toke = ""
            return self.tokens
            
        # if self.toke in sorted(self.varss, key=len, reverse=True):
        #     print(sorted(self.varss, key=len, reverse=True))
        #     self.tokens[len(self.tokens)-1].append("VAR;"+self.toke)
        #     self.toke = ""
        #     return self.tokens
       
        
        if self.toke[0] == '"' and self.toke[len(self.toke)-1] == '"' and len(self.toke) > 1:
            self.tokens[len(self.tokens)-1].append("STR;"+self.toke.replace('"',""))
            self.toke = ""
            return self.tokens
        
        if self.check_sign(self.current_letter) or self.counter == len(self.text[self.line_counter])-1 and self.toke[:-1].replace(".","").isnumeric():
            
            if self.toke[:-1].replace(" ","").count(".") == 1:
                if self.check_sign(self.toke[-1]):
                    self.tokens[len(self.tokens)-1].append("FLOAT;"+self.toke[:-1].replace(" ",""))
                else:
                    self.tokens[len(self.tokens)-1].append("FLOAT;"+self.toke.replace(" ",""))
                            
            elif self.toke[:-1].replace(" ","").isnumeric():
                if self.check_sign(self.toke[-1]):
                    self.tokens[len(self.tokens)-1].append("INT;"+self.toke[:-1].replace(" ",""))
                else:
                    self.tokens[len(self.tokens)-1].append("INT;"+self.toke.replace(" ",""))

            if self.check_sign(self.toke[-1]):
                
                if self.toke.replace(" ","")[:-1] in sorted(self.varss, key=len, reverse=True):
                    
                    self.tokens[len(self.tokens)-1].append("VAR;"+self.toke.replace(" ","")[:-1])
                self.tokens[len(self.tokens)-1].append(self.toke[-1])
                
            self.toke = ""
            return self.tokens

        #Create a Var section
        
        
        if len(self.tokens[self.line_counter]) > 0:
            if self.tokens[self.line_counter][0] == "var" or self.tokens[self.line_counter][0] == "connec":

                var_t_type = self.tokens[self.line_counter][0]
                if var_t_type == "var":
                    
                    var_t_name = (self.text[self.line_counter][self.text[self.line_counter].index(var_t_type)+4:].split("="))[0][:-1]
                    var_t_carry = (self.text[self.line_counter][self.text[self.line_counter].index(var_t_type)+4:].split("="))[1][1:]
                elif var_t_type == "connec":
                    var_t_name = self.text[self.line_counter][self.text[self.line_counter].index(var_t_type)+7:].split("=")[0][:-1]
                    var_t_carry = self.text[self.line_counter][self.text[self.line_counter].index(var_t_type)+7:].split("=")[1][1:]
                toke_t = ""
                var_t_tokens = []
                counter_t = 0
                sum = 0
                #Name Checking:
                if var_t_name in self.varss.keys():
                    raise Exception (ERROR_NAME+" Error: Var name '"+var_t_name+"',Has been manufactored before and can not again")
                else:
                    
                    for number in ["1","2","3","4","5","6","7","8","9","0"]:
                        if number in var_t_name:
                            
                            
                            raise Exception(ERROR_NAME+" Error: Var name '"+var_t_name+"',Contains invalid characters")
                            
                            # raise_error("Var name '"+var_t_name+"',Contains invalid characters")
                            
                            
            try: 
                for letter in var_t_carry:
                    toke_t += letter
                    counter_t += 1 
                    
                    if toke_t == " ":
                        toke_t = ""
                    elif toke_t in self.varss.keys():
                        if var_t_type == "connec":
                            var_t_tokens.append("CONNEC;"+toke_t)
                        elif var_t_type == "var":
                            ###################################################################
                            sum = eval(str(self.calc(self.varss[toke_t].carry)).replace("]",")").replace("[","(").replace(",","").replace("'",""))
                            try:
                                if isinstance(sum,float):
                                    var_t_tokens.append("FLOAT;"+str(sum))
                                elif isinstance(sum,int):
                                    var_t_tokens.append("INT;"+str(sum))
                                
                            except Exception as e:
                                print("PROBLEM",e)
                            print(sum)
                            # var_t_tokens.append("VAR;"+toke_t)
                            # var_t_tokens.append()
                        toke_t = ""
                    elif toke_t[0] == '"' and toke_t[len(toke_t)-1] == '"' and len(toke_t) > 1:
                        
                        var_t_tokens.append("STR;"+toke_t.replace('"',""))
                        toke_t = ""
                    elif self.check_sign(letter) or counter_t == len(var_t_carry):
                        
                        if toke_t[:-1].replace(" ","").count(".") == 1:
                            if self.check_sign(toke_t[-1]):
                                var_t_tokens.append("FLOAT;"+toke_t[:-1].replace(" ",""))
                            else:
                                var_t_tokens.append("FLOAT;"+toke_t.replace(" ",""))
                            
                        elif toke_t[:-1].replace(" ","").isnumeric() or toke_t.replace(" ","").isnumeric():
                            if self.check_sign(toke_t[-1]):
                                var_t_tokens.append("INT;"+toke_t[:-1].replace(" ",""))
                            else:
                                var_t_tokens.append("INT;"+toke_t.replace(" ",""))
                        if self.check_sign(toke_t[-1]):
                            var_t_tokens.append(toke_t[-1])
                        toke_t = ""

                self.varss[var_t_name] = Var(var_t_name,var_t_tokens,var_t_type)
                self.tokens[len(self.tokens)-1].append(var_t_name)
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
        if len(new_text) == 0:
            raise Exception(ERROR_NAME+" Error: File is empty")
        return new_text

def lex(text):
    lexer_t = Lexer(text) 
    lexer_t.run()
    for key in lexer_t.varss.keys():
        print(lexer_t.varss[key].name,lexer_t.varss[key].carry,lexer_t.varss[key].type)
    print(lexer_t.tokens)
    # print(lexer_t.varss)
def run(file_to_run):
    
    check_file(file_to_run)
    lex(read_file(file_to_run))
    

if __name__ == "__main__":
    run(argv[1])




"""
Hello there!
I think u r on deafen...
U can type stuff in the chat if u want
I am still waiting for u to undeafen...(23:00)

"""