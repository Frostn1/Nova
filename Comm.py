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
        self.callback = []
    
    
    

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
            "link",
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
        
        for toke in self.key_words:
            
            if self.toke == toke:
                
                self.tokens[len(self.tokens)-1].append(self.toke)
                self.toke = ""
                return self.tokens

        if self.toke == " ":
            self.toke = ""
            return self.tokens
        if len(self.toke) > 1:
            if self.toke[0] == '"' and self.toke[len(self.toke)-1] == '"' and len(self.toke) > 1:
                self.tokens[len(self.tokens)-1].append("STR;"+self.toke.replace('"',""))
                self.toke = ""
                return self.tokens
        
        if self.check_sign(self.current_letter) or self.counter == len(self.text[self.line_counter])-1 and (self.toke[:-1].replace(".","").isnumeric() or self.toke.replace(".","").isnumeric()) or self.toke.replace(" ","")[-1] == '"' and len(self.toke.replace(" ","")) > 1:
 
            if self.toke[:-1].replace(" ","").count(".") == 1:
                if self.check_sign(self.toke[-1]):
                    self.tokens[len(self.tokens)-1].append("FLOAT;"+self.toke[:-1].replace(" ","")) 
                else:
                    self.tokens[len(self.tokens)-1].append("FLOAT;"+self.toke.replace(" ",""))                 
            elif self.toke.replace(" ","")[:-1].isnumeric() or self.toke.replace(" ","").isnumeric():
                
                if self.check_sign(self.toke[-1]) or self.toke[-1] == '"':
                    self.tokens[len(self.tokens)-1].append("INT;"+self.toke[:-1].replace(" ",""))
                    if self.toke[-1] == '"':
                        self.toke = self.toke[-1] 
                else:
                    
                    self.tokens[len(self.tokens)-1].append("INT;"+self.toke.replace(" ",""))
                    
            try:
                if self.check_sign(self.toke[-1]) or self.toke[-1] == '"':
                    
                    if self.toke.replace(" ","")[:-1] in sorted(self.varss.keys(), key=len, reverse=True):
                        
                        if self.toke[-1] == '"':
                            self.tokens[len(self.tokens)-1].append("VAR;"+self.toke.replace(" ","")[:-1])
                            self.toke = self.toke[-1]
                        else:
                            self.tokens[len(self.tokens)-1].append("VAR;"+self.toke.replace(" ","")[:-1])
                            self.tokens[len(self.tokens)-1].append(self.toke[-1])
                            self.toke = ""
                    else:
                        if self.check_sign(self.toke[-1]):
                            self.tokens[len(self.tokens)-1].append(self.toke[-1])
                            self.toke = ""
                else:
                    self.toke = ""
            except:
                pass
            
            return self.tokens

        #Create a Var section
        
        
        if len(self.tokens) > self.line_counter and len(self.tokens[self.line_counter]) > 0:
            if self.tokens[self.line_counter][0] == "var" or self.tokens[self.line_counter][0] == LINKED_VAR_NAME:

                var_t_type = self.tokens[self.line_counter][0]
                if var_t_type == "var":
                    
                    var_t_name = (self.text[self.line_counter][self.text[self.line_counter].index(var_t_type)+4:].split("="))[0][:-1]
                    var_t_carry = (self.text[self.line_counter][self.text[self.line_counter].index(var_t_type)+4:].split("="))[1][1:]

                elif var_t_type == LINKED_VAR_NAME:
                    var_t_name = self.text[self.line_counter][self.text[self.line_counter].index(var_t_type)+5:].split("=")[0][:-1]
                    var_t_carry = self.text[self.line_counter][self.text[self.line_counter].index(var_t_type)+5:].split("=")[1][1:]
                toke_t = ""
                var_t_tokens = []
                counter_t = 0
                sum = 0
                final_sum = 0
                
                #Name Checking:
                if var_t_name in self.varss.keys():
                    raise Exception (ERROR_NAME+" Error: Var name '"+var_t_name+"',Has been manufactored before and can not again")
                else:
                    for number in ["1","2","3","4","5","6","7","8","9","0"]:
                        if number in var_t_name:
        
                            raise Exception(ERROR_NAME+" Error: Var name '"+var_t_name+"',Contains invalid characters")
                            
                for letter in var_t_carry:
                    toke_t += letter
                    counter_t += 1 
                    
                    if toke_t == " ":
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
                        else:
                            if not self.check_sign(toke_t.replace(" ","")[-1]) and toke_t not in sorted(self.varss.keys(), key=len, reverse=True):
                                print(toke_t)
                                raise Exception(ERROR_NAME+" Error: Var used without being manufactored")
                        if self.check_sign(toke_t[-1]):
                             
                            if toke_t.replace(" ","")[:-1] in sorted(self.varss.keys(), key=len, reverse=True):
                                
                                if var_t_type == LINKED_VAR_NAME:
                                    
                                    var_t_tokens.append("LINK;"+toke_t.replace(" ","")[:-1])
                                elif var_t_type == "var":
                                    
                                    try:
                                        sum = eval(str(self.calc(self.varss[toke_t.replace(" ","")[:-1]].carry)).replace("]",")").replace("[","(").replace(",","").replace("'",""))
                                    except Exception as e:
                                        raise Exception(ERROR_NAME + " Error: Cant connect str to int/float.",)

                                    if isinstance(sum,float):
                                        var_t_tokens.append("FLOAT;"+str(sum))
                                    elif isinstance(sum,int):
                                        var_t_tokens.append("INT;"+str(sum)) 
                                    sum = 0

                                    # var_t_tokens.append("VAR;"+toke_t)
                                    # var_t_tokens.append()
                            
                                
                            var_t_tokens.append(toke_t[-1])
                            toke_t = ""
                        elif counter_t == len(var_t_carry) and var_t_type == LINKED_VAR_NAME and toke_t in sorted(self.varss.keys(), key=len, reverse=True):
                                
                                var_t_tokens.append("LINK;"+toke_t.replace(" ",""))
               
                try:
                    if var_t_type == "var":
                        sum = str(eval(str(self.calc(var_t_tokens)).replace("]",")").replace("[","(").replace(",","").replace("'","").replace("^","**")))
                        if sum.count(".") == 1:
                            final_sum = ["FLOAT;" + sum]
                        else :
                            final_sum = ["INT;" + sum]
                        self.varss[var_t_name] = Var(var_t_name,final_sum,var_t_type)
                    else:
                        
                        self.varss[var_t_name] = Var(var_t_name,var_t_tokens,var_t_type)
                except Exception as e:
                    self.varss[var_t_name] = Var(var_t_name,var_t_tokens,var_t_type)
                    pass
                
                self.tokens[len(self.tokens)-1].append(var_t_name)
                self.toke = ""
                return "con"  
        return self.tokens
        
       
class Parser:
    def __init__(self,tokens,varss):
        self.tokens = tokens[:-1]
        self.varss = varss
        self.line_counter = 0
    def run(self):
        # for key in self.varss.keys():
        #     print(self.varss[key].carry)
        
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
        if line[0] == "typeln(":
            print(final_prin)
        elif line[0] == "type(":
            print(final_prin,end="")
    def alter_var(self,line):
        
        if len(line) < 3:
            raise Exception(ERROR_NAME + " Error: To few of arguments given.")
        elif line[1] != "=":
            raise Exception(ERROR_NAME + " Error: Assigment sign has not been found.")
        else:
            if self.varss[line[0][line[0].index(";")+1:]].type == "connec":
                raise Exception(ERROR_NAME + " Error: Cant modify a CONNEC var, as its a CONST.")
            else:
                new_carry = ""
                new_type = ""
                final_carry = []
                for word in line[2:]:
                    if "VAR" in word:
                        new_carry += str(eval(str(self.calc(self.varss[word[word.index(";")+1:]].carry)).replace("]",")").replace("[","(").replace(",","").replace("'","")))
                    else:
                        new_carry += str(word[word.index(";")+1:])
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

    def input_data(self,line):
        if len(line) != 3:
            raise Exception(ERROR_NAME + " Error: number of arguments given to the 'get' function is wrong.")
        else:
            
            if line[1][line[1].index(";")+1:] in sorted(self.varss.keys(), key=len, reverse=True):
                
                if self.varss[line[1][line[1].index(";")+1:]].type == "var":
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
                    self.varss[line[1][line[1].index(";")+1:]].carry = final_carry
                else:
                    raise Exception(ERROR_NAME + " Error: Cant modify a CONNEC var, as its a CONST.")
            else:
                raise Exception(ERROR_NAME + " Error: The Var given to the get function hasnt been manufactored yet.")
    def execute(self,line):
        
        if len(line) < 1:
            pass
        elif line[0] == "type(" or line[0] == "typeln(":
            self.typing(line)
        elif line[0] == "var" or line[0] == LINKED_VAR_NAME:
            pass
        elif line[0] == "get(":
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
    parse(tokens,varss)
    

if __name__ == "__main__":
    run(argv[1])
