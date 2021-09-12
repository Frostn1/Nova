class stack:
    def __init__(self):
        self.size = 0
        self.content = list()
    def is_empty(self):
        return not bool(self.content)
    def push(self,elem):
        self.content.append(elem)
        self.size = len(self.content)-1
    def pop_(self):
        if not self.is_empty():

            elem = self.content.pop()
            size = len(self.content)-1
            return elem
        else:
            return None
    def peek(self):
        if not self.is_empty():
            return self.content[-1]
        else:
            return None
    def display(self):
        if not self.is_empty():
            return self.content
        else:
            return None


class convertor:

    @staticmethod
    def postinfix(expressionlist):
        changer = stack()
        new_exp = list()
        operator_precedence = ['+','-','*','/','^',]
        for k in expressionlist:
            if k in operator_precedence:
                prec_check = operator_precedence.index(k)
                while True:
                    curr_op = changer.peek()
                    if curr_op in operator_precedence:
                        curr_op_val = operator_precedence.index(curr_op)
                        if curr_op_val >= prec_check:
                            add = changer.pop_()
                            new_exp.append(add)
                        else:
                            break
                    else:
                        break         
                changer.push(k)
            elif k == '(':
                changer.push(k)
            elif k == ')':
                while True:
                    if changer.peek() == '(':
                        changer.pop_()
                        break
                    else:
                        add = changer.pop_()
                        new_exp.append(add)
            else:
                new_exp.append(k)
        while not changer.is_empty():
            new_exp.append(changer.pop_())
        return new_exp

print(convertor.postinfix([i for i in '1+2*(4*3)']))
