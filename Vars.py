class Var:

    def __init__(self,name,carry,type_):
        self.name = name
        self.carry = carry
        self.type = type_
        self.callback = {}
        self.created = False

class Vector:
    pass