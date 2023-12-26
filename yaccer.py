import ply.yacc as yacc
from node import *
from lexer import Lexer

tokens = Lexer.tokens
literals = Lexer.literals


class Yacc(object):
    tokens = tokens
    literals = literals

    def p_program(self, p):
        """program : stmts"""
        p[0] = p[1]

    def p_empty(self, p):
        """empty :"""
        pass

    def p_stmts(self, p):
        """
        stmts   : stmt stmts
                | empty
        """
        if p[1]:
            p[0] = Node('stmts', left=p[1], right=p[2])

    def p_stmt(self, p):
        """
        stmt    :  exp
                | printStmt
                | defStmt
        """
        p[0] = p[1]

    def p_defStmt(self, p):
        """
        defStmt : '(' DEFINE variable exp ')'
        """
        p[0] = Node('define', left=p[3], right=p[4])

    def p_ID(self, p):
        """
        variable : ID
        funName : ID
        id : ID
        """
        p[0] = Node(p[1])

    def p_printStmt(self, p):
        """
        printStmt   : '(' PRINT_NUM exp ')'
                    | '(' PRINT_BOOL exp ')'
        """
        p[0] = Node(p[2], left=p[3])

    def p_exp(self, p):
        """
        exp : boolVal
            | number
            | numOP
            | logicalOP
            | ifExp
            | variable
            | funExp
            | funCall
        """
        p[0] = p[1]

    def p_valueNode(self, p):
        """
        number : NUMBER
        boolVal : BOOL_VAL
        """
        p[0] = Node(p[1])

    def p_numOP(self, p):
        """
        numOP   : '(' '+' exp exps ')'
                | '(' '-' exp exp ')'
                | '(' '*' exp exps ')'
                | '(' '/' exp exp ')'
                | '(' MODULES exp exp ')'
                | '(' '>' exp exp ')'
                | '(' '<' exp exp ')'
                | '(' '=' exp exps ')'
        """
        p[0] = Node(p[2], left=p[3], right=p[4])

    def p_logicalOP(self, p):
        """
        logicalOP   : '(' AND exp exps ')'
                    | '(' OR exp exps ')'
                    | '(' NOT exp ')'
        """
        if p[2] == 'and' or p[2] == 'or':
            p[0] = Node(p[2], left=p[3], right=p[4])
        if p[2] == 'not':
            p[0] = Node(p[2], left=p[3])

    def p_exps(self, p):
        """
        exps    :  exp exps
                | exp empty
        """
        if p[2]:
            p[0] = Node('exps', left=p[1], right=p[2])
        else:
            p[0] = p[1]

    def p_tokens(self, p):
        """
        params  : exp params
                | empty
        ids     : id ids
                | empty
        """
        if p[1]:
            p[0] = Node([p[1]]+p[2].value if p[2] else [p[1]])

    def p_ifExp(self, p):
        """
        ifExp : '(' IF test_esp then_esp else_esp ')'
        """

        p[0] = Node('if_exp', left=Node([p[3], p[4], p[5]]))

    def p_alt_esp(self, p):
        """
        test_esp : exp
        then_esp : exp
        else_esp : exp
        """
        p[0] = p[1]

    def p_funBody(self, p):
        """
        fun_body : stmts
        """
        p[0] = p[1]


    def p_funExp(self, p):
        """
        funExp : '(' FUN fun_ids fun_body ')'
        """
        p[0] = Node(Function(p[3], p[4]))


    def p_funCall(self, p):
        """
        funCall : '(' funExp params ')'
                | '(' funName params ')'
        """
        if p[3]:
            p[0] = Node('call_func', left=p[2], right=p[3])
        else:
            p[0] = Node('call_func', left=p[2], right=Node([]))

    def p_fun_ids(self, p):
        """
        fun_ids : '(' ids ')'
        """
        p[0] = p[2]

    def p_error(self, p):
        print(f'Syntax error at {p.value!r}')

    def build(self, **kwargs):
        Yacc.parser = yacc.yacc(module=self, **kwargs)

    def test(self, data):
        print(Yacc.parser.parse(data))

    def get_ast_tree(self, data):
        return Yacc.parser.parse(data)

