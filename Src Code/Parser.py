import random
import Vars
ERROR_NAME = "Goblin"
COMPILER_NAME = "Commander"

LINKED_VAR_NAME = "link"
REGULAR_VAR_NAME = "var"
ERRORS_FILE = ""#Errors.txt

class Parser:
    def __init__(self,tokens,varss,semi):
        if tokens[-1] == []:
            self.tokens = tokens[:-1]
        else:
            self.tokens = tokens
        self.varss = varss
        self.line_counter = 0
        self.when_flag = 0
        self.when_line = 0
        if semi != []:
            self.init_var(semi)
        if ERRORS_FILE.strip() != "":
            # print("YAP")
            with open(ERRORS_FILE,"r") as file1:
                self.errors = file1.readlines()
        self.if_section = []
        self.vars_when = []
        self.when_lines = []
    def init_var(self,varss):
        for var in varss:
            self.varss[var] = Vars.Var(var,[],"")

    def run(self):
        # for key in self.varss.keys():
        #     print("VAR",self.varss[key].carry,self.varss[key].type,self.varss[key].callback)
        
        # print(self.tokens)
        for line in self.tokens:
            self.execute(line) 
            self.line_counter += 1
        if self.when_flag:
            # print("WHEN IS",self.when_flag)
            self.Error("When statement was not close by a 'end' statement at line ")
    
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
        self.sign_list = ["+","-","*","/","^","(",")","=","!",">","<"]
        for sign in self.sign_list:
            if sign == toke:
                return sign
        return False
    def Error(self,error_type):
        if ERRORS_FILE.strip() != "":
            raise Exception(self.errors[random.randint(0,len(self.errors)-1)]+ error_type)
        else:
            raise Exception(ERROR_NAME + " Error: " + error_type)
    def print_var(self):

        for key in self.varss.keys():
            print(key,self.varss[key].carry,self.varss[key].created)
        print("[End]")

    def check_callback(self,var_name):
        # print("YCK",var_name,self.varss[var_name].callback)
        current_toke = ""
        current_counter = 0
        final_carry = []
        # pre_vars = []
        # print("CHECK VAR",self.varss[var_name].callback.keys(),var_name)
        # try:
        #     print(self.varss[var_name].callback)
        # except:
        #     print("UTTO")
        for key in self.varss[var_name].callback.keys():
            #print("KEY IS",key)
            final_carry = []
            for letter in key:
                current_toke += letter
                current_counter += 1
                if self.check_sign(letter) or len(key) == current_counter:
                    #print("CURR",current_toke)
                    if current_toke[:-1] in sorted(self.varss,key=len,reverse=True) or current_toke in sorted(self.varss,key=len,reverse=True):

                        if current_toke in sorted(self.varss,key=len,reverse=True):
                            line = self.varss[current_toke].carry
                        elif current_toke[:-1] in sorted(self.varss,key=len,reverse=True):
                            
                            line = self.varss[current_toke[:-1]].carry
                        new_carry = ""
                        
                        for word in line:
                            
                            if "VAR" in word:
                                new_carry += str(eval(str(self.calc(self.varss[word[word.index(";")+1:]].carry)).replace("]",")").replace("[","(").replace(",","").replace("'","")))
                            else:
                                
                                try:
                                    new_carry += str(word[word.index(";")+1:])
                                except:
                                    new_carry += str(word)
                        try:
                            new_carry = eval(new_carry)
                        except:
                            pass
                            
                        final_carry.append(str(new_carry))
                        if self.check_sign(current_toke[-1]):
                            final_carry.append(str(current_toke[-1]))
                        current_toke = ""
                    elif self.check_sign(letter):
                        final_carry += letter
                        current_toke = ""
                    else:
                        #print("HEY",current_toke,letter) 
                        final_carry.append(current_toke)
                        current_toke = ""
                


            # print("Final",final_carry,var_name,"".join(final_carry), 10<=9)
            try:
                if eval("".join(final_carry)):
                    #print("IS TRUE")
                    pre_vars = self.varss.keys()
                    # print("PRE",pre_vars,var_name,key_)

                    parser_t = Parser(self.varss[var_name].callback[key],self.varss,[])
                    parser_t.run()
                    post_vars = parser_t.varss.keys()
            except:
                pass 
                      
            
        
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

                                exp.append(self.calc(self.varss[line[i][line[i].index(";")+1:].replace(" ","")].carry))
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
                        final_exp = ""
                        exp = []
                        
            counter += 1
        if line[0] == "println":
            print(final_prin)
        elif line[0] == "print":
            print(final_prin,end="")

    def alter_var(self,line,type_):
        # print("ALTERING VAR",line)
        if len(line) < 3:
            
            self.Error("To few of arguments given.")
        elif line[1] != "=":
            self.Error("Assigment sign has not been found.")
        else:
            if line[0][line[0].index(";")+1:] in self.varss.keys() and (type_ == LINKED_VAR_NAME or self.varss[line[0][line[0].index(";")+1:]].type == LINKED_VAR_NAME):
                if self.varss[line[0][line[0].index(";")+1:]].created:
                    
                    self.Error("Cant modify a "+LINKED_VAR_NAME+" var, as its a CONST.")
                else:
                    # print("[CREATING CONST]",line[0][line[0].index(";")+1:])
                    self.varss[line[0][line[0].index(";")+1:]] = Vars.Var(line[0][line[0].index(";")+1:],[],LINKED_VAR_NAME)
                    self.varss[line[0][line[0].index(";")+1:]].carry = line[2:]
                    self.varss[line[0][line[0].index(";")+1:]].created = True
                    
            else:
                if line[0][line[0].index(";")+1:] not in self.varss.keys():
                    self.varss[line[0][line[0].index(";")+1:]] = Vars.Var(line[0][line[0].index(";")+1:],[],REGULAR_VAR_NAME)
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
                self.varss[line[0][line[0].index(";")+1:]].type = type_
                
                # self.print_var()
                try:
                    self.check_callback(line[0][line[0].index(";")+1:])
                except:
                    print("PRO")

    def input_data(self,line):
        if len(line) != 4:
            self.Error("Number of arguments given to the 'get' function is wrong.")
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
                    try:
                        self.check_callback(line[2][line[2].index(";")+1:])
                    except:
                        print("PROB")
                else:
                    self.Error("Cant modify a "+ LINKED_VAR_NAME +" var, as its a CONST.")
            else:
                self.Error("The Var given to the get function hasnt been manufactored yet.")
    
    def when_state(self,line):

        if "when" in line[0]:
            
            self.vars_when.append([])
            self.when_line_num = self.line_counter
            if_section = ""
            for word in line[2:-2]:
                if word != " ":
                    if word == "#":
                        if_section += word.replace("#","==")
                    elif self.check_sign(word):
                        if_section += word
                    elif "or" == word or "and" == word or "not" == word:
                       if_section += " " + word + " "
                    if word != " " and ";" in word and word[word.index(";")+1:] in sorted(self.varss,key=len,reverse=True):
                        
                        if_section += word[word.index(";")+1:]
                        
                        self.vars_when[len(self.vars_when)-1].append(word[word.index(";")+1:])
                    elif word != " " and ";" in word:
                        if_section += word[word.index(";")+1:]      
            self.if_section += [if_section]
        else:
            
            self.when_lines.append(line)
            
    def end_state(self,line):
        self.when_flag -= 1
        # print("ENDING",self.when_flag)
        # print("Lines",self.when_lines)
        # print("NO",self.when_lines,self.if_section,self.vars_when[self.when_flag])
        # print("HMMMMMM",self.vars_when,self.when_flag,self.if_section) 
        for var in self.vars_when[self.when_flag]:
            self.varss[var].callback[self.if_section[self.when_flag]] = self.when_lines
        # print(var,self.varss[var].callback)
        self.if_section = []
        self.vars_when = []

    def execute(self,line):
        
        if len(line) < 1:
            pass
        elif line[0] == "when":
            
            self.when_flag += 1
            # print("WHENNNN",self.when_flag)
            self.when_state(line)
        elif self.when_flag and line != ["end"]:
            # print("HMM I AM HERE",line)
            self.when_state(line)
        elif line[0] == "print" or line[0] == "println":
            self.typing(line)
        elif line[0] == "var" or line[0] == LINKED_VAR_NAME:
            self.alter_var(line[1:],line[0])
        elif line[0] == "get":
           self.input_data(line)
        elif line[0] == "end":
            
            self.end_state(line)
        elif line[0][line[0].index(";")+1:] in sorted(self.varss.keys(), key=len, reverse=True):
            self.alter_var(line,self.varss[line[0][line[0].index(";")+1:]].type)