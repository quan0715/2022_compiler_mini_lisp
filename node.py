class Function:
    def __init__(self, args, fun_body):
        self.args = args
        self.fun_body = fun_body
        self.id_table = {}

    def __repr__(self):
        return f"func: {self.args} {self.fun_body}"


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f'Node: {self.value}'


class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f'{self.name} {self.value}'