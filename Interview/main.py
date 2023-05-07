class Stack:
    def __init__(self):
        self.__stack = []

    def is_empty(self):
        return not bool(self.__stack)

    def push(self, elem):
        self.__stack.append(elem)

    def pop(self):
        return self.__stack.pop()

    def peek(self):
        return self.__stack[-1]

    @property
    def size(self):
        return len(self.__stack)


def check_staples(bracket_string: str) -> str:
    stack = Stack()
    opened = '({['
    closed = ')}]'
    for i in bracket_string:
        if i in opened:
            stack.push(i)
        elif i in closed:
            index = closed.index(i)
            if stack.size > 0 and opened[index] == stack.peek():
                stack.pop()
            else:
                return "Несбалансированно"
    else:
        return "Cбалансированно" if stack.size == 0 else "Несбалансированно"


if __name__ == '__main__':
    
    set_staples = ['(((([{}]))))', '[([])((([[[]]])))]{()}', '[([])((([[[]]])))]{()}', '}{}', '{{[(])]}}', '[[{())}]']
    for elem in set_staples:
        print(f"'{elem}' - {check_staples(elem)}")
