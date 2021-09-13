import errorhandling
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
        operator_precedence = {}
        operator_precedence['!'] = 5
        operator_precedence['^'] = 4
        operator_precedence['/'] = 3
        operator_precedence['*'] = 3
        operator_precedence['+'] = 2
        operator_precedence['-'] = 2
        for k in expressionlist:
            if k in operator_precedence:
                prec_check = operator_precedence[k]
                while True:
                    curr_op = changer.peek()
                    if curr_op in operator_precedence:
                        curr_op_val = operator_precedence[curr_op]
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

class calc:


    @staticmethod
    def factorial(n):
        # base case
        if n == 1:
            return 1
        # recursive case
        else:
            return n * calc.factorial(n-1)
    @staticmethod
    def calc_(op1, op, op2):
        if op == '+':
            return op1 + op2
        elif op == '-':
            return op1 - op2
        elif op == '*':
            return op1 * op2
        elif op == '/':
            return op1 / op2
        elif op == '^':
            return op1 ** op2

    @staticmethod
    def calc_post(postfix_list, errorhandler, section, pos, variables):

        def getType(value,_vars):
            if value.isnumeric() or ('.' in value and value[value.index('.')+1:].isnumeric() and value[:value.index('.')].isnumeric()):
                return "number"
            elif value.isidentifier():
                return _vars[value].type

        operand_stack = stack()

        for val in postfix_list:
            if val in '+-*/^!':
                if val == '!':
                    op = operand_stack.pop_()
                    if op.isnumeric():
                        res = calc.factorial(int(op))
                        operand_stack.push(str(res))
                    else:
                        errorhandler.add(errorhandling.Error(section, "fatal", "variable type doesnt match for factorial", (pos[0], pos[1]), op))
                else:
                    op2 = operand_stack.pop_()
                    op1 = operand_stack.pop_()
                    types = getType(op2, variables), getType(op1, variables)
                    if types[0] == types[1]:
                        if types[0] == 'number':
                            res = calc.calc_(float(op1), val, float(op2))
                        else:
                            res = calc.calc_(op1, val, op2)
                        operand_stack.push(str(res))
                    else:
                        errorhandler.add(errorhandling.Error(section, "fatal", "variable type missmatch", (pos[0], pos[1]), op1 + ' ' + op2))
            else:
                operand_stack.push(val)
        res = float(operand_stack.content[-1])
        int_res = int(res)
        if int_res == res:
            return int_res
        return res

# print(calc.calc_post(convertor.postinfix([i for i in '3!+2*(4*3)']), errorhandling.ErrorHandler(), "semantic", (0,0), {}))
