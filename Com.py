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
            
        
           

    # def advance(self):
    #     self.counter += 1
    #     if self.line_counter < len(self.text)-1:
    #         if self.counter >= len(self.text[self.line_counter]):
    #             self.line_counter += 1
    #             try:
    #                 self.current_letter = self.text[self.line_counter][0]
                    
    #             except:
    #                 pass
    #             self.counter = 0
    #             self.toke = ""
    #         else:
    #             self.current_letter = self.text[self.line_counter][self.counter]
    #         self.toke += self.current_letter
    #     else:
    #         if self.counter < len(self.text[self.line_counter]):
    #             self.current_letter = self.text[self.line_counter][self.counter]
    #             self.toke += self.current_letter

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
        
        self.flag = 0
        if self.toke.replace(" ","") in self.key_words or (self.toke.replace(" ","")[:-1] in self.key_words and self.counter != len(self.text[self.line_counter])-1):
            if self.check_sign(self.toke.replace(" ","")[-1]):
                self.tokens[len(self.tokens)-1].append(self.toke.replace(" ","")[:-1])
            else:
                self.tokens[len(self.tokens)-1].append(self.toke.replace(" ",""))
            self.flag = 1
            
        elif  (self.tokens[len(self.tokens)-1] == [REGULAR_VAR_NAME] or self.tokens[len(self.tokens)-1] == [LINKED_VAR_NAME]) and self.toke not in sorted(self.varss,key=len,reverse=True) and len(self.toke.replace(" ","")) > 0:
            
            self.varss[self.toke.replace(" ","")] = Var(self.toke,[],self.tokens[len(self.tokens)-1])
            self.tokens[len(self.tokens)-1].append(self.toke.replace(" ",""))
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
        elif self.toke.replace(" ","").isnumeric():
            self.tokens[len(self.tokens)-1].append("INT;" + self.toke.replace(" ",""))
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

# def parse(tokens,varss):
#     parser_t = Parser(tokens,varss)
#     parser_t.run()
def run(file_to_run):
    
    check_file(file_to_run)
    tokens,varss = lex(read_file(file_to_run))
    print(tokens)
    # parse(tokens,varss)
    

if __name__ == "__main__":
    run(argv[1])