ERROR_NAME = "Goblin"
COMPILER_NAME = "Commander"

LINKED_VAR_NAME = "link"
REGULAR_VAR_NAME = "var"


class Parser:
    def __init__(self,tokens,varss):
        self.tokens = tokens[:-1]
        self.varss = varss
        self.line_counter = 0
        self.when_flag = False
        self.when_line = 0
    def run(self):
        # for key in self.varss.keys():
        #     print("VAR",self.varss[key].carry,self.varss[key].type)
        
        # print(self.tokens)
        for line in self.tokens:
            self.execute(line) 
            self.line_counter += 1
        if self.when_flag:
            raise SyntaxError(ERROR_NAME + " Error: When statement was not close by a 'end' statement at line " + str(self.when_line+1))
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
        print(line)
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
    def when_state(self,line):
        self.when_flag = True
        self.when_line = self.line_counter
        if_section = ""
        self.vars_when = []
        if "when" in line[0]:
            print("THIUS LINE",line[2:-2])
            for word in line[2:-2]:
                
                if word == "#":
                        if_section += word.replace("#","==")
                if word != " " and word[word.index(";")+1:] in sorted(self.varss,key=len,reverse=True):
                    if_section += word[word.index(";")+1:]
                    self.vars_when.append(word[word.index(";")+1:])
                
                    
                        
            
            print("First line")
            print(self.vars_when)
            print("YEP",if_section)
            
        else:
            print("Nope",line)
        # print("When statement",line)
    def end_state(self,line):
        self.when_flag = False
        print("End statement",line)
    def execute(self,line):
        
        if len(line) < 1:
            pass
        elif self.when_flag and line != ["end"]:
            self.when_state(line)
        elif line[0] == "type" or line[0] == "typeln":
            self.typing(line)
        elif line[0] == "var" or line[0] == LINKED_VAR_NAME:
            self.alter_var(line[1:])
        elif line[0] == "get":
           self.input_data(line)
        elif line[0] == "when":
            self.when_state(line)
        elif line[0] == "end":
            self.end_state(line)
        elif line[0][line[0].index(";")+1:] in sorted(self.varss.keys(), key=len, reverse=True):
            self.alter_var(line)