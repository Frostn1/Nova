import Vars
ERROR_NAME = "Goblin"
COMPILER_NAME = "Commander"

LINKED_VAR_NAME = "link"
REGULAR_VAR_NAME = "var"



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
            ":",
            "Vector",
            "sin",
            "cos"
        ]

        self.tokens = [[]]
        self.varss = {}
        self.vector_state = False
    
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
            self.vector_state = False 
            check = ""
        
    def check_sign(self,toke):
        self.sign_list = ["+","-","*","/","^","(",")","=","#"]
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
        print(self.tokens,self.toke + "__")
        type_t = ""
        self.flag = 0
        if self.toke.replace(" ","") in self.key_words or (self.toke.replace(" ","")[:-1] in self.key_words and self.counter != len(self.text[self.line_counter])-1):
            if self.check_sign(self.toke.replace(" ","")[-1]):
                if self.toke.replace(" ","")[:-1] == "Vector":
                    print("YEP1")
                    self.vector_state = True
                self.tokens[len(self.tokens)-1].append(self.toke.replace(" ","")[:-1])
            else:
                if self.toke.replace(" ","") == "Vector":
                    print("YEP")
                    self.vector_state = True
                self.tokens[len(self.tokens)-1].append(self.toke.replace(" ",""))
            self.flag = 1
            
        elif  (self.tokens[len(self.tokens)-1] == [REGULAR_VAR_NAME] or self.tokens[len(self.tokens)-1] == [LINKED_VAR_NAME]) and self.toke not in sorted(self.varss,key=len,reverse=True) and len(self.toke.replace(" ","")) > 0:
            
            if self.check_sign(self.toke[-1]):
                type_t = self.tokens[len(self.tokens)-1][0]
                self.varss[self.toke.replace(" ","")] = Vars.Var(self.toke.replace(" ","")[:-1],[],type_t)
                type_t = ""
                self.tokens[len(self.tokens)-1].append("VAR;"+self.toke.replace(" ","")[:-1])
            else:
                type_t = self.tokens[len(self.tokens)-1][0]
                self.varss[self.toke.replace(" ","")] = Vars.Var(self.toke.replace(" ",""),[],type_t)
                type_t = ""
                self.tokens[len(self.tokens)-1].append("VAR;"+self.toke.replace(" ",""))
            self.flag = 1
        elif len(self.toke.strip()) > 1 and self.toke.lstrip()[0] == '"' and (self.toke[-1] == '"' or self.toke[-2] == '"'):
            if self.check_sign(self.toke.strip()[-1]):
                self.tokens[len(self.tokens)-1].append("STR;" + self.toke.strip()[1:-2])
                
            else:
                self.tokens[len(self.tokens)-1].append("STR;" + self.toke.strip()[1:-1])
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
        elif self.vector_state:
            if self.check_sign(self.toke[-1]):
                self.tokens[len(self.tokens)-1].append("ARG;"+self.toke.replace(" ","")[:-1]) 
            else:
                self.tokens[len(self.tokens)-1].append("ARG;"+self.toke.replace(" ",""))
            self.flag = 1
        try: 
            if self.toke[-1] != " " and bool(self.check_sign(self.toke.replace(" ","")[-1])):
                print(self.toke)
                self.tokens[len(self.tokens)-1].append(self.toke.replace(" ","")[-1])
                self.flag = 1
        except:
            pass   

        # print(self.toke)
        if self.flag:
            self.toke = ""
        return self.tokens