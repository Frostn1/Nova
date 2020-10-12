from sys import *
import os
ERROR_NAME = "Goblin"
COMPILER_NAME = "Commander"

LINKED_VAR_NAME = "link"
REGULAR_VAR_NAME = "var"
class Var:

    def __init__(self,name,carry,type_):
        self.name = name
        self.carry = carry
        self.type = type_
        self.callback = {}
        self.created = False
    
    

class Lexer:
    def __init__(self,text):
        self.text = text
        # self.current_letter = text[0][0]
        self.toke = ""
        self.counter = 0
        self.line_counter = 0
        self.key_words = [
            "typeln",
            "type",
            "var",
            "link",
            "get",
            "when",
            "end",
            "#",
            ":"
        ]

        self.tokens = [[]]
        self.varss = {}
    
    def run(self):

        check = ""
        for line in self.text:  
            for letter in line:
                # print(self.toke,"TOKEN")
                self.toke += letter
                if self.check_sign(str(letter)) or letter == " " or self.counter == len(line)-1:
                    check = self.check_toke()
                self.counter += 1
            self.toke = ""
            self.line_counter += 1
            self.counter = 0
            self.tokens.append([]) 
            check = ""
        
    def check_sign(self,toke):
        self.sign_list = ["+","-","*","/","^","(",")","="]
        for sign in self.sign_list:
            if sign == toke:
                return sign
        return False
    
    def calc(self,list_):

        sum = []
        for word in list_:
            
            if "VAR" in word or "LINK" in word:
                sum.append(self.calc(self.varss[word[word.index(";")+1:]]))
            else:
                try:
                    sum.append(word[word.index(";")+1:])
                except:
                    sum.append(word)
                    pass
        return sum
    def check_toke(self):
        type_t = ""
        self.flag = 0
        if self.toke.replace(" ","") in self.key_words or (self.toke.replace(" ","")[:-1] in self.key_words and self.counter != len(self.text[self.line_counter])-1):
            if self.check_sign(self.toke.replace(" ","")[-1]):
                self.tokens[len(self.tokens)-1].append(self.toke.replace(" ","")[:-1])
            else:
                self.tokens[len(self.tokens)-1].append(self.toke.replace(" ",""))
            self.flag = 1
            
        elif  (self.tokens[len(self.tokens)-1] == [REGULAR_VAR_NAME] or self.tokens[len(self.tokens)-1] == [LINKED_VAR_NAME]) and self.toke not in sorted(self.varss,key=len,reverse=True) and len(self.toke.replace(" ","")) > 0:
            
            if self.check_sign(self.toke[-1]):
                type_t = self.tokens[len(self.tokens)-1][0]
                self.varss[self.toke.replace(" ","")] = Var(self.toke.replace(" ","")[:-1],[],type_t)
                type_t = ""
                self.tokens[len(self.tokens)-1].append("VAR;"+self.toke.replace(" ","")[:-1])
            else:
                type_t = self.tokens[len(self.tokens)-1][0]
                self.varss[self.toke.replace(" ","")] = Var(self.toke.replace(" ",""),[],type_t)
                type_t = ""
                self.tokens[len(self.tokens)-1].append("VAR;"+self.toke.replace(" ",""))
            self.flag = 1
        elif len(self.toke.strip()) > 1 and self.toke.lstrip()[0] == '"' and (self.toke[-1] == '"' or self.toke[-2] == '"'):
            if self.check_sign(self.toke.strip()[-1]):
                self.tokens[len(self.tokens)-1].append("STR;" + self.toke.strip()[:-1])
            else:
                self.tokens[len(self.tokens)-1].append("STR;" + self.toke.strip())
            self.flag = 1
        elif self.toke.replace(" ","")[:-1] in sorted(self.varss,key=len,reverse=True)  or self.toke.replace(" ","") in sorted(self.varss,key=len,reverse=True):
            
            if self.check_sign(self.toke.replace(" ","")[-1]):
                self.tokens[len(self.tokens)-1].append("VAR;" + self.toke.replace(" ","")[:-1])
            else:
                self.tokens[len(self.tokens)-1].append("VAR;" + self.toke.replace(" ",""))
            self.flag = 1
        elif self.toke.replace(" ","").isnumeric() or self.toke[:-1].replace(" ","").isnumeric():
            if self.toke.replace(" ","").isnumeric():
                self.tokens[len(self.tokens)-1].append("INT;" + self.toke.replace(" ",""))
            else:
                self.tokens[len(self.tokens)-1].append("INT;" + self.toke.replace(" ","")[:-1])
            self.flag = 1
        elif self.toke.replace(" ","").count(".") == 1:
            self.tokens[len(self.tokens)-1].append("FLOAT;" + self.toke.replace(" ",""))
            self.flag = 1
        try: 
            if self.toke != " " and bool(self.check_sign(self.toke.replace(" ","")[-1])) and self.toke[0] != '"':
                self.tokens[len(self.tokens)-1].append(self.toke.replace(" ","")[-1])
                self.flag = 1
        except:
            pass   

        # print(self.toke)
        if self.flag:
            self.toke = ""
        return self.tokens

class Parser:
    def __init__(self,tokens,varss):
        self.tokens = tokens[:-1]
        self.varss = varss
        self.line_counter = 0
    def run(self):
        # for key in self.varss.keys():
        #     print("VAR",self.varss[key].carry,self.varss[key].type)
        
        # print(self.tokens)
        for line in self.tokens:
            self.execute(line) 
            self.line_counter += 1
    def calc(self,list_):

        sum = []
        for word in list_:
            
            if "VAR" in word or "LINK" in word:
                sum.append(self.calc(self.varss[word[word.index(";")+1:]].carry))
            else:
                try:
                    sum.append(word[word.index(";")+1:])
                except:
                    sum.append(word)
                    pass
        return sum
    
    def simplify(self,list1,list2=[]):
    
        for element in list1:
            if type(element)!=list:
                list2.append(element)
            else:
                self.simplify(element,list2)
        return list2
    def check_sign(self,toke):
        self.sign_list = ["+","-","*","/","^","(",")","="]
        for sign in self.sign_list:
            if sign == toke:
                return sign
        return False

    def typing(self,line):
        final_prin = ""
        counter = 0
        state = 0
        exp = []
        i = 0
        final_exp = ""
        for param in line[1:]:
            
            if "STR" in param:
                state = 0
                final_prin += param[param.index(";")+1:]
            else:
                
                if state == 0:
                    if not self.check_sign(param):
                        i = counter +1
                        
                        state = 1
                        while "STR" not in line[i]  and i < len(line)-1:
                            
                            if "VAR" in line[i] or "LINK" in line[i]:
                                
                                exp.append(self.calc(self.varss[line[i][line[i].index(";")+1:]].carry))
                            elif "INT" in line[i] or "FLOAT" in line[i]:
                                exp.append(line[i][line[i].index(";")+1:])
                            else:
                                exp.append(line[i])
                            i += 1
                        
                        exp = self.simplify(exp,[])
                        for param in exp:
                            
                            final_exp += param
                        try:
                            final_exp = str(eval(final_exp))
                        except:
                            final_exp = ""
                            for param in exp:
                                if not self.check_sign(param):
                                    final_exp += param

                        final_prin += final_exp

            counter += 1
        if line[0] == "typeln":
            print(final_prin)
        elif line[0] == "type":
            print(final_prin,end="")

    def alter_var(self,line):
        
        if len(line) < 3:
            raise Exception(ERROR_NAME + " Error: To few of arguments given.",self.line_counter)
        elif line[1] != "=":
            raise Exception(ERROR_NAME + " Error: Assigment sign has not been found.",self.line_counter)
        else:
            if self.varss[line[0][line[0].index(";")+1:]].type == LINKED_VAR_NAME:
                if self.varss[line[0][line[0].index(";")+1:]].created:
                    raise Exception(ERROR_NAME + " Error: Cant modify a "+LINKED_VAR_NAME+" var, as its a CONST.",self.line_counter)
                else:
                    self.varss[line[0][line[0].index(";")+1:]].carry = line[2:]
                    self.varss[line[0][line[0].index(";")+1:]].created = True
                    
            else:
                
                new_carry = ""
                new_type = ""
                final_carry = []
                for word in line[2:]:
                    
                    if "VAR" in word:
                        new_carry += str(eval(str(self.calc(self.varss[word[word.index(";")+1:]].carry)).replace("]",")").replace("[","(").replace(",","").replace("'","")))
                    else:
                        
                        try:
                            new_carry += str(word[word.index(";")+1:])
                        except:
                            new_carry += str(word)
                try:
                    new_carry = eval(new_carry)
                    if isinstance(new_carry,float):
                        new_type = "FLOAT;"
                    elif isinstance(new_carry,int):
                        new_type = "INT;"
                except:
                    new_type = "STR;"
                
                    
                final_carry.append(new_type + str(new_carry))
                
                self.varss[line[0][line[0].index(";")+1:]].carry = final_carry
                self.varss[line[0][line[0].index(";")+1:]].created = True

    def input_data(self,line):
        if len(line) != 4:
            raise Exception(ERROR_NAME + " Error: number of arguments given to the 'get' function is wrong.",self.line_counter)
        else:
            
            if line[2][line[2].index(";")+1:] in sorted(self.varss.keys(), key=len, reverse=True):
                
                if self.varss[line[2][line[2].index(";")+1:]].type == "var":
                    new_type = ""
                    final_carry = []
                    inp = input()
                    
                    try:
                        inp = eval(inp)
                        if isinstance(inp,float):
                            new_type = "FLOAT;"
                        elif isinstance(inp,int):
                            new_type = "INT;"
                    except:
                        new_type = "STR;"
                    final_carry.append(new_type + str(inp))
                    self.varss[line[2][line[2].index(";")+1:]].carry = final_carry
                else:
                    raise Exception(ERROR_NAME + " Error: Cant modify a "+ LINKED_VAR_NAME +" var, as its a CONST.",self.line_counter)
            else:
                raise Exception(ERROR_NAME + " Error: The Var given to the get function hasnt been manufactored yet.",self.line_counter)
    def execute(self,line):
        
        if len(line) < 1:
            pass
        elif line[0] == "type" or line[0] == "typeln":
            self.typing(line)
        elif line[0] == "var" or line[0] == LINKED_VAR_NAME:
            self.alter_var(line[1:])
        elif line[0] == "get":
           self.input_data(line)
        elif line[0][line[0].index(";")+1:] in sorted(self.varss.keys(), key=len, reverse=True):
            self.alter_var(line)



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
    lexer_t = Lexer(text) 
    lexer_t.run()
    return lexer_t.tokens, lexer_t.varss

def parse(tokens,varss):
    parser_t = Parser(tokens,varss)
    parser_t.run()
def run(file_to_run):
    
    check_file(file_to_run)
    tokens,varss = lex(read_file(file_to_run))
    # print(tokens)
    # print(varss)
    # for var in varss.keys():
    #     print("HMMM",varss[var].name,varss[var].carry,varss[var].type)
    parse(tokens,varss)
    

if __name__ == "__main__":
    run(argv[1])