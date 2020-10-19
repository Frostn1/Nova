class Var:

    def __init__(self,name,carry,type_):
        self.name = name
        self.carry = carry
        self.type = type_
        self.callback = {}
        self.created = False
    
class Vector_N:
    def __init__(self,line_x,line_y,varss):
        self.line_x = line_x
        self.line_y = line_y
        self.varss = varss
        self.created = False
        self.print()
    def print(self):
        print("LINE X",self.line_x)
        print("LINE Y",self.line_y)
        print(self.varss)
    pass

class Vector_L:
    pass


