from lexer import Lexer
from yaccer import Yacc
import sys
from node import *
ID_table = {}
op_map = {'mod': '%', '/': '//', '-': '-', '>': '>', '<': '<', '+': '+', '*': '*', '=': '==', 'and': '&', 'or': '|', 'not':'not'}


def get_node_value(node, id_table):
    if isinstance(node.value, str):
        if node.value in id_table.keys():
            return id_table[node.value].value
        if node.value in ID_table.keys():
            return ID_table[node.value].value
        if node.value in ['call_func', 'if_exp', 'define'] or node.value in op_map.keys():
            vec = []
            traverse_op_tree(node)
            traverse_tree(node, vec, id_table)
            return vec[-1].value
    return node.value


def get_op_exp(vec, op, id_table):
    if op == 'not':
        v1 = get_node_value(vec.pop(-1), id_table)
        if isinstance(v1, bool):
            v3 = not v1
            vec.append(Node(bool(v3)))
            return
        raise TypeError
    v2 = get_node_value(vec.pop(-1), id_table)
    v1 = get_node_value(vec.pop(-1), id_table)
    if op in ["and", "or"]:
        if type(v2) == bool and type(v1) == bool:
            v3 = eval(f"{v1} {op_map[op]} {v2}")
            vec.append(Node(bool(v3)))
            return
        raise TypeError
    elif op in ["+", "-", "*", "/", "mod"]:
        if type(v2) == int and type(v1) == int:
            v3 = eval(f"{v1} {op_map[op]} {v2}")
            vec.append(Node(int(v3)))
            return
        raise TypeError
    elif op in ["<", ">", "="]:
        if type(v2) == int and type(v1) == int:
            v3 = eval(f"{v1} {op_map[op]} {v2}")
            vec.append(Node(bool(v3)))
            return
        raise TypeError


def if_exp(vec, id_table):
    exps = get_node_value(vec.pop(-1), id_table)
    condition = get_node_value(exps[0], id_table)
    if type(condition) == bool:
        if condition:
            vec.append(exps[1])
        else:
            vec.append(exps[2])
    else:
        raise TypeError


def print_stmt(op, vec, id_table):
    v = get_node_value(vec.pop(-1), id_table)
    if op == 'print-num':
        print(int(v))
    elif op == 'print-bool':
        print("#t" if v else "#f")


def fun_call(vec, id_table):
    params = get_node_value(vec.pop(-1), id_table)
    func = get_node_value(vec.pop(-1), id_table)
    temp_id_table = {}
    if func.args:
        for k, v in zip(func.args.value, params):
            v = get_node_value(v, id_table)
            temp_id_table[k.value] = Variable(k.value, v)
    t = []
    traverse_op_tree(func.fun_body)
    temp_id_table.update(func.id_table)
    traverse_tree(func.fun_body, t, temp_id_table)
    r = get_node_value(t[-1], temp_id_table)
    if isinstance(r, Function):
        r.id_table = temp_id_table
    vec.append(Node(r))


def def_stmt(vec, id_table):
    value = get_node_value(vec.pop(-1), id_table)
    id_name = get_node_value(vec.pop(-1), id_table)
    ID_table.update({id_name: Variable(id_name, value)})


def traverse_tree(node, vec, id_table):
    if node.left:
        traverse_tree(node.left, vec, id_table)
    if node.right:
        traverse_tree(node.right, vec, id_table)
    if isinstance(node.value, str) and node.value.startswith('print-'):
        print_stmt(node.value, vec, id_table)
    if isinstance(node.value, str) and node.value in op_map.keys():
        get_op_exp(vec, node.value, id_table)
    elif isinstance(node.value, str) and node.value == 'define':
        def_stmt(vec, id_table)
    elif isinstance(node.value, str) and node.value == "if_exp":
        if_exp(vec, id_table)
    elif isinstance(node.value, str) and node.value == "call_func":
        fun_call(vec, id_table)

    elif node.left is None and node.right is None:
        vec.append(node)


def traverse_op_tree(node, op=None):
    if node.left:
        traverse_op_tree(node.left, op)
    if isinstance(node.value, str) and node.value in op_map.keys():
        op = node.value
    if isinstance(node.value, str) and node.value == 'exps':
        if op:
            node.value = op
    if node.right:
        traverse_op_tree(node.right, op)


def main():
    l: Lexer = Lexer()
    l.build()
    data = sys.stdin.read()
    y: Yacc = Yacc()
    y.build()
    vec = []
    tree = y.get_ast_tree(data)
    try:
        if tree:
            traverse_op_tree(tree)
            traverse_tree(tree, vec, ID_table)
    except TypeError:
        print("TypeError")


if __name__ == '__main__':
    main()
